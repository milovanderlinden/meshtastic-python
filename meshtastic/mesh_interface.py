"""Mesh Interface class
"""

import collections
import json
import logging
import random
import sys
import threading
import time
from datetime import datetime

from typing import Any, Callable, Dict, List, Optional, Union

import google.protobuf.json_format
import timeago  # type: ignore[import-untyped]
from pubsub import pub  # type: ignore[import-untyped]
from tabulate import tabulate

from . import (
    node,
    mesh_pb2,
    portnums_pb2,
    telemetry_pb2
)

from .constants import BROADCAST_ADDR, LOCAL_ADDR, BROADCAST_NUM, publishingThread
from .info import Info
from .known_protocol import protocols
from .response_handler import ResponseHandler
from .schemas.mesh import NodeInfo, Channel, Config, ModuleConfig, Position, DeviceMetadata, MyNodeInfo

from .util import (
    Acknowledgment,
    Timeout,
    our_exit,
    stripnl, clean_nones,
)


class MeshInterface:
    """Interface class for meshtastic devices

    Properties:

    isConnected
    nodes
    debugOut
    """
    my_node_info: MyNodeInfo = None  # We don't have device info yet
    my_node: NodeInfo = None
    localNode: node.Node
    metadata: DeviceMetadata = DeviceMetadata()  # Metadata object
    nodes: Dict[int, NodeInfo] = {}  # Dict with nodes by number
    channels: List[Channel] = [Channel()] * 8  # 8 empty channel definitions
    config: Config = Config()  # Config object
    module_config: ModuleConfig = ModuleConfig()  # ModuleConfig Object

    class MeshInterfaceError(Exception):
        """An exception class for general mesh interface errors"""

        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    def __init__(self, debugOut=None, noProto: bool = False) -> None:
        """Constructor

        Keyword Arguments:
            noProto -- If True, don't try to run our protocol on the
                       link - just be a dumb serial client.
        """
        self.debugOut = debugOut
        self.isConnected: threading.Event = threading.Event()
        self.noProto: bool = noProto
        self.localNode = node.Node(self, -1)
        self.metadata: Optional[mesh_pb2.DeviceMetadata] = None  # We don't have device metadata yet
        self.responseHandlers: Dict[int, ResponseHandler] = {}  # A map from request ID to the handler
        self.failure = (
            None  # If we've encountered a fatal exception it will be kept here
        )
        self._timeout: Timeout = Timeout()
        self._acknowledgment: Acknowledgment = Acknowledgment()
        self.heartbeatTimer: Optional[threading.Timer] = None
        self.currentPacketId: int = random.randint(0, 0xFFFFFFFF)
        self.configId: Optional[int] = None

        self.queueStatus: Optional[mesh_pb2.QueueStatus] = None
        self.queue: collections.OrderedDict = collections.OrderedDict()
        self._localChannels = None

    def getNode(self, node_num: Union[int, str]) -> Union[None, NodeInfo]:
        """Return a node object which contains device settings and channel info"""
        if isinstance(node_num, str):
            if node_num in (LOCAL_ADDR, BROADCAST_ADDR):
                return self.nodes[self.my_node_info.my_node_num]
        else:
            return self.nodes[node_num]

    def close(self):
        """Shutdown this interface"""
        if self.heartbeatTimer:
            self.heartbeatTimer.cancel()

        self._sendDisconnect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and exc_value is not None:
            logging.error(
                f"An exception of type {exc_type} with value {exc_value} has occurred"
            )
        if traceback is not None:
            logging.error(f"Traceback: {traceback}")
        self.close()

    def showInfo(self, file=sys.stdout) -> Info:  # pylint: disable=W0613
        """Show human-readable summary about this object"""

        _out: Info = Info(**{
            "myNodeInfo": self.my_node_info,
            "myNode": self.getNode(self.my_node_info.my_node_num),
            "nodes": list(self.nodes.values()),
            "channels": self.channels
        })
        # _json = json.dumps(clean_nones(_out), default=str)
        return _out

    def showNodes(self, include_my: bool = True, file=sys.stdout) -> str:  # pylint: disable=W0613
        """Show table summary of nodes in mesh"""

        def formatFloat(value, precision=2, unit="") -> Optional[str]:
            """Format a float value with precision."""
            return f"{value:.{precision}f}{unit}" if value else None

        def getLH(ts) -> Optional[str]:
            """Format last heard"""
            return (
                datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else None
            )

        def getTimeAgo(ts) -> Optional[str]:
            """Format how long ago have we heard from this node (aka timeago)."""
            return (
                timeago.format(datetime.fromtimestamp(ts), datetime.now())
                if ts
                else None
            )

        rows: List[Dict[str, Any]] = []
        if self.nodesByNum:
            logging.debug(f"self.nodes:{self.nodes}")
            for _node in self.nodesByNum.values():
                if not include_my and node == self.my_node.nodeNum:
                    continue

                row = {"N": 0, "User": f"UNK: {_node['num']}", "ID": f"!{_node['num']:08x}"}

                user = _node.get("user")
                if user:
                    row.update(
                        {
                            "User": user.get("longName", "N/A"),
                            "AKA": user.get("shortName", "N/A"),
                            "ID": user["id"],
                        }
                    )

                pos = _node.get("position")
                if pos:
                    row.update(
                        {
                            "Latitude": formatFloat(pos.get("latitude"), 4, "°"),
                            "Longitude": formatFloat(pos.get("longitude"), 4, "°"),
                            "Altitude": formatFloat(pos.get("altitude"), 0, " m"),
                        }
                    )

                metrics = _node.get("deviceMetrics")
                if metrics:
                    battery_level = metrics.get("batteryLevel")
                    if battery_level is not None:
                        if battery_level == 0:
                            battery_string = "Powered"
                        else:
                            battery_string = str(battery_level) + "%"
                        row.update({"Battery": battery_string})
                    row.update(
                        {
                            "Channel util.": formatFloat(
                                metrics.get("channelUtilization"), 2, "%"
                            ),
                            "Tx air util.": formatFloat(
                                metrics.get("airUtilTx"), 2, "%"
                            ),
                        }
                    )

                row.update(
                    {
                        "SNR": formatFloat(_node.get("snr"), 2, " dB"),
                        "Hops Away": _node.get("hopsAway", "0/unknown"),
                        "Channel": _node.get("channel", 0),
                        "LastHeard": getLH(_node.get("lastHeard")),
                        "Since": getTimeAgo(_node.get("lastHeard")),
                    }
                )

                rows.append(row)

        rows.sort(key=lambda r: r.get("LastHeard") or "0000", reverse=True)
        for i, row in enumerate(rows):
            row["N"] = i + 1

        table = tabulate(rows, headers="keys", missingval="N/A", tablefmt="fancy_grid")
        print(table)
        return table

    def sendText(
            self,
            text: str,
            destinationId: Union[int, str] = BROADCAST_ADDR,
            wantAck: bool = False,
            wantResponse: bool = False,
            onResponse: Optional[Callable[[mesh_pb2.MeshPacket], Any]] = None,
            channelIndex: int = 0,
    ):
        """Send a utf8 string to some other node, if the node has a display it
           will also be shown on the device.

        Arguments:
            text {string} -- The text to send

        Keyword Arguments:
            destinationId {nodeId or nodeNum} -- where to send this
                                                 message (default: {BROADCAST_ADDR})
            portNum -- the application portnum (similar to IP port numbers)
                       of the destination, see portnums.proto for a list
            wantAck -- True if you want the message sent in a reliable manner
                       (with retries and ack/nak provided for delivery)
            wantResponse -- True if you want the service on the other side to
                            send an application layer response

        Returns the sent packet. The id field will be populated in this packet
        and can be used to track future message acks/naks.
        """

        return self.sendData(
            text.encode("utf-8"),
            destinationId,
            portNum=portnums_pb2.PortNum.TEXT_MESSAGE_APP,
            wantAck=wantAck,
            wantResponse=wantResponse,
            onResponse=onResponse,
            channelIndex=channelIndex,
        )

    def sendData(
            self,
            data,
            destinationId: Union[int, str] = BROADCAST_ADDR,
            portNum: portnums_pb2.PortNum.ValueType = portnums_pb2.PortNum.PRIVATE_APP,
            wantAck: bool = False,
            wantResponse: bool = False,
            onResponse: Optional[Callable[[mesh_pb2.MeshPacket], Any]] = None,
            channelIndex: int = 0,
    ):
        """Send a data packet to some other node

        Keyword Arguments:
            data -- the data to send, either as an array of bytes or
                    as a protobuf (which will be automatically
                    serialized to bytes)
            destinationId {nodeId or nodeNum} -- where to send this
                    message (default: {BROADCAST_ADDR})
            portNum -- the application portnum (similar to IP port numbers)
                    of the destination, see portnums.proto for a list
            wantAck -- True if you want the message sent in a reliable
                    manner (with retries and ack/nak provided for delivery)
            wantResponse -- True if you want the service on the other
                    side to send an application layer response
            onResponse -- A closure of the form funct(packet), that will be
                    called when a response packet arrives (or the transaction
                    is NAKed due to non receipt)
            channelIndex - channel number to use

        Returns the sent packet. The id field will be populated in this packet
        and can be used to track future message acks/naks.
        """

        if getattr(data, "SerializeToString", None):
            logging.debug(f"Serializing protobuf as data: {stripnl(data)}")
            data = data.SerializeToString()

        logging.debug(f"len(data): {len(data)}")
        logging.debug(
            f"mesh_pb2.Constants.DATA_PAYLOAD_LEN: {mesh_pb2.Constants.DATA_PAYLOAD_LEN}"
        )
        if len(data) > mesh_pb2.Constants.DATA_PAYLOAD_LEN:
            raise MeshInterface.MeshInterfaceError("Data payload too big")

        if (
                portNum == portnums_pb2.PortNum.UNKNOWN_APP
        ):  # we are now strict in relation to port numbers
            our_exit("Warning: A non-zero port number must be specified")

        mesh_packet = mesh_pb2.MeshPacket()
        mesh_packet.channel = channelIndex
        mesh_packet.decoded.payload = data
        mesh_packet.decoded.portnum = portNum
        mesh_packet.decoded.want_response = wantResponse
        mesh_packet.id = self._generatePacketId()

        if onResponse is not None:
            logging.debug(f"Setting a response handler for requestId {mesh_packet.id}")
            self._addResponseHandler(mesh_packet.id, onResponse)
        p = self._sendPacket(mesh_packet, destinationId, wantAck=wantAck)
        return p

    def sendPosition(
            self,
            latitude: float = 0.0,
            longitude: float = 0.0,
            altitude: int = 0,
            timeSec: int = 0,
            destinationId: Union[int, str] = BROADCAST_ADDR,
            wantAck: bool = False,
            wantResponse: bool = False,
            channelIndex: int = 0,
    ):
        """
        Send a position packet to some other node (normally a broadcast)

        Also, the device software will notice this packet and use it to automatically
        set its notion of the local position.

        If timeSec is not specified (recommended), we will use the local machine time.

        Returns the sent packet. The id field will be populated in this packet and
        can be used to track future message acks/naks.
        """
        p = mesh_pb2.Position()
        if latitude != 0.0:
            p.latitude_i = int(latitude / 1e-7)
            logging.debug(f"p.latitude_i:{p.latitude_i}")

        if longitude != 0.0:
            p.longitude_i = int(longitude / 1e-7)
            logging.debug(f"p.longitude_i:{p.longitude_i}")

        if altitude != 0:
            p.altitude = int(altitude)
            logging.debug(f"p.altitude:{p.altitude}")

        if timeSec == 0:
            timeSec = int(time.time())  # returns unix timestamp in seconds
        p.time = timeSec
        logging.debug(f"p.time:{p.time}")

        if wantResponse:
            onResponse = self.onResponsePosition
        else:
            onResponse = None

        d = self.sendData(
            p,
            destinationId,
            portNum=portnums_pb2.PortNum.POSITION_APP,
            wantAck=wantAck,
            wantResponse=wantResponse,
            onResponse=onResponse,
            channelIndex=channelIndex,
        )
        if wantResponse:
            self.waitForPosition()
        return d

    def onResponsePosition(self, p):
        """on response for position"""
        if p["decoded"]["portnum"] == 'POSITION_APP':
            self._acknowledgment.receivedPosition = True
            position = mesh_pb2.Position()
            position.ParseFromString(p["decoded"]["payload"])

            ret = "Position received: "
            if position.latitude_i != 0 and position.longitude_i != 0:
                ret += f"({position.latitude_i * 10 ** -7}, {position.longitude_i * 10 ** -7})"
            else:
                ret += "(unknown)"
            if position.altitude != 0:
                ret += f" {position.altitude}m"

            if position.precision_bits not in [0, 32]:
                ret += f" precision:{position.precision_bits}"
            elif position.precision_bits == 32:
                ret += " full precision"
            elif position.precision_bits == 0:
                ret += " position disabled"

            print(ret)

        elif p["decoded"]["portnum"] == 'ROUTING_APP':
            if p["decoded"]["routing"]["errorReason"] == 'NO_RESPONSE':
                our_exit("No response from node. At least firmware 2.1.22 is required on the destination node.")

    def sendTraceRoute(self, dest: Union[int, str], hopLimit: int, channelIndex: int = 0):
        """Send the trace route"""
        r = mesh_pb2.RouteDiscovery()
        self.sendData(
            r,
            destinationId=dest,
            portNum=portnums_pb2.PortNum.TRACEROUTE_APP,
            wantResponse=True,
            onResponse=self.onResponseTraceRoute,
            channelIndex=channelIndex,
        )
        # extend timeout based on number of nodes, limit by configured hopLimit
        waitFactor = min(len(self.nodes) - 1 if self.nodes else 0, hopLimit)
        self.waitForTraceRoute(waitFactor)

    def onResponseTraceRoute(self, p):
        """on response for trace route"""
        routeDiscovery = mesh_pb2.RouteDiscovery()
        routeDiscovery.ParseFromString(p["decoded"]["payload"])
        asDict = google.protobuf.json_format.MessageToDict(routeDiscovery)

        print("Route traced:")
        routeStr = self._nodeNumToId(p["to"])
        if "route" in asDict:
            for nodeNum in asDict["route"]:
                routeStr += " --> " + self._nodeNumToId(nodeNum)
        routeStr += " --> " + self._nodeNumToId(p["from"])
        print(routeStr)

        self._acknowledgment.receivedTraceRoute = True

    def sendTelemetry(self, destinationId: Union[int, str] = BROADCAST_ADDR, wantResponse: bool = False,
                      channelIndex: int = 0):
        """Send telemetry and optionally ask for a response"""
        _telemetry = telemetry_pb2.Telemetry()

        if self.nodes is not None:
            _node: NodeInfo = next(n for n in self.nodes.values() if n.num == self.my_node.num)
            if _node is not None:
                metrics = _node.device_metrics
                if metrics:
                    if metrics.battery_level is not None:
                        _telemetry.device_metrics.battery_level = metrics.battery_level
                    if metrics.voltage is not None:
                        _telemetry.device_metrics.voltage = metrics.voltage
                    if metrics.channel_utilization is not None:
                        _telemetry.device_metrics.channel_utilization = metrics.channel_utilization
                    if metrics.air_util_tx is not None:
                        _telemetry.device_metrics.air_util_tx = metrics.air_util_tx

        if wantResponse:
            on_response = self.onResponseTelemetry
        else:
            on_response = None

        self.sendData(
            _telemetry,
            destinationId=destinationId,
            portNum=portnums_pb2.PortNum.TELEMETRY_APP,
            wantResponse=wantResponse,
            onResponse=on_response,
            channelIndex=channelIndex,
        )
        if wantResponse:
            self.waitForTelemetry()

    def onResponseTelemetry(self, p):
        """on response for telemetry"""
        if p["decoded"]["portnum"] == 'TELEMETRY_APP':
            self._acknowledgment.receivedTelemetry = True
            telemetry = telemetry_pb2.Telemetry()
            telemetry.ParseFromString(p["decoded"]["payload"])

            print("Telemetry received:")
            if telemetry.device_metrics.battery_level is not None:
                print(f"Battery level: {telemetry.device_metrics.battery_level:.2f}%")
            if telemetry.device_metrics.voltage is not None:
                print(f"Voltage: {telemetry.device_metrics.voltage:.2f} V")
            if telemetry.device_metrics.channel_utilization is not None:
                print(
                    f"Total channel utilization: {telemetry.device_metrics.channel_utilization:.2f}%"
                )
            if telemetry.device_metrics.air_util_tx is not None:
                print(f"Transmit air utilization: {telemetry.device_metrics.air_util_tx:.2f}%")

        elif p["decoded"]["portnum"] == 'ROUTING_APP':
            if p["decoded"]["routing"]["errorReason"] == 'NO_RESPONSE':
                our_exit("No response from node. At least firmware 2.1.22 is required on the destination node.")

    def _addResponseHandler(self, requestId: int, callback: Callable):
        self.responseHandlers[requestId] = ResponseHandler(callback)

    def _sendPacket(self, meshPacket: mesh_pb2.MeshPacket, destination: Union[int, str] = BROADCAST_ADDR,
                    wantAck: bool = False):
        """Send a MeshPacket to the specified node (or if unspecified, broadcast).
        You probably don't want this - use sendData instead.

        Returns the sent packet. The id field will be populated in this packet and
        can be used to track future message acks/naks.
        """
        _node_num: int = 0
        # We allow users to talk to the local node before we've completed the full connection flow...
        if self.my_node_info is not None and destination != self.my_node_info.my_node_num:
            self._waitConnected()

        _to_radio = mesh_pb2.ToRadio()

        if destination is None:
            our_exit("Warning: destinationId must not be None")
        elif isinstance(destination, int):
            _node_num = destination
        elif destination == BROADCAST_ADDR:
            _node_num = BROADCAST_NUM
        elif destination == LOCAL_ADDR:
            if self.my_node_info:
                _node_num = self.my_node_info.num
            else:
                our_exit("Warning: No my_node_info found.")
        # A simple hex style nodeid - we can parse this without needing the DB
        elif destination.startswith("!"):
            _node_num = int(destination[1:], 16)
        else:
            if self.nodes:
                _node = self.nodes[destination]
                if _node is None:
                    our_exit(f"Warning: NodeId {destination} not found")
                else:
                    _node_num = _node.num
            else:
                logging.warning("Warning: There were no self.nodes.")

        meshPacket.to = _node_num

        # if the user hasn't set an ID for this packet (likely and recommended),
        # we should pick a new unique ID so the message can be tracked.
        if meshPacket.id == 0:
            meshPacket.id = self._generatePacketId()

        _to_radio.packet.CopyFrom(meshPacket)
        if self.noProto:
            logging.warning(
                f"Not sending packet because protocol use is disabled by noProto"
            )
        else:
            logging.debug(f"Sending packet: {stripnl(meshPacket)}")
            self._sendToRadio(_to_radio)
        return meshPacket

    def waitForConfig(self):
        """Block until radio config is received. Returns True if config has been received."""
        success = (
                self._timeout.waitForSet(self, attrs=("my_node_info", "nodes"))
                and self.localNode.waitForConfig()
        )
        if not success:
            raise MeshInterface.MeshInterfaceError("Timed out waiting for interface config")

    def waitForAckNak(self):
        """Wait for the ack/nak"""
        success = self._timeout.waitForAckNak(self._acknowledgment)
        if not success:
            raise MeshInterface.MeshInterfaceError("Timed out waiting for an acknowledgment")

    def waitForTraceRoute(self, waitFactor):
        """Wait for trace route"""
        success = self._timeout.waitForTraceRoute(waitFactor, self._acknowledgment)
        if not success:
            raise MeshInterface.MeshInterfaceError("Timed out waiting for traceroute")

    def waitForTelemetry(self):
        """Wait for telemetry"""
        success = self._timeout.waitForTelemetry(self._acknowledgment)
        if not success:
            raise MeshInterface.MeshInterfaceError("Timed out waiting for telemetry")

    def waitForPosition(self):
        """Wait for position"""
        success = self._timeout.waitForPosition(self._acknowledgment)
        if not success:
            raise MeshInterface.MeshInterfaceError("Timed out waiting for position")

    def _waitConnected(self, timeout=30.0):
        """Block until the initial node db download is complete, or timeout
        and raise an exception"""
        if not self.noProto:
            if not self.isConnected.wait(timeout):  # timeout after x seconds
                raise MeshInterface.MeshInterfaceError("Timed out waiting for connection completion")

        # If we failed while connecting, raise the connection to the client
        if self.failure:
            raise self.failure

    def _generatePacketId(self) -> int:
        """Get a new unique packet ID"""
        if self.currentPacketId is None:
            raise MeshInterface.MeshInterfaceError("Not connected yet, can not generate packet")
        else:
            self.currentPacketId = (self.currentPacketId + 1) & 0xFFFFFFFF
            return self.currentPacketId

    def _disconnected(self):
        """Called by subclasses to tell clients this interface has disconnected"""
        self.isConnected.clear()
        publishingThread.queueWork(
            lambda: pub.sendMessage("meshtastic.connection.lost", interface=self)
        )

    def _startHeartbeat(self):
        """We need to send a heartbeat message to the device every X seconds"""

        def callback():
            self.heartbeatTimer = None
            prefs = self.localNode.localConfig
            i = prefs.power.ls_secs / 2
            logging.debug(f"Sending heartbeat, interval {i}")
            if i != 0:
                self.heartbeatTimer = threading.Timer(i, callback)
                self.heartbeatTimer.start()
                p = mesh_pb2.ToRadio()
                p.heartbeat.CopyFrom(mesh_pb2.Heartbeat())
                self._sendToRadio(p)

        callback()  # run our periodic callback now, it will make another timer if necessary

    def _connected(self):
        """Called by this class to tell clients we are now fully connected to a node"""
        # (because I'm lazy) _connected might be called when remote Node
        # objects complete their config reads, don't generate redundant isConnected
        # for the local interface
        if not self.isConnected.is_set():
            self.isConnected.set()
            self._startHeartbeat()
            publishingThread.queueWork(
                lambda: pub.sendMessage(
                    "meshtastic.connection.established", interface=self
                )
            )

    def _startConfig(self):
        """Start device packets flowing"""
        start_config = mesh_pb2.ToRadio()
        self.configId = random.randint(0, 0xFFFFFFFF)
        start_config.want_config_id = self.configId
        self._sendToRadio(start_config)

    def _sendDisconnect(self):
        """Tell device we are done using it"""
        m = mesh_pb2.ToRadio()
        m.disconnect = True
        self._sendToRadio(m)

    def _queueHasFreeSpace(self) -> bool:
        # We never got queueStatus, maybe the firmware is old
        if self.queueStatus is None:
            return True
        return self.queueStatus.free > 0

    def _queueClaim(self) -> None:
        if self.queueStatus is None:
            return
        self.queueStatus.free -= 1

    def _sendToRadio(self, toRadio: mesh_pb2.ToRadio) -> None:
        """Send a ToRadio protobuf to the device"""
        if self.noProto:
            logging.warning(
                f"Not sending packet because protocol use is disabled by noProto"
            )
        else:
            # logging.debug(f"Sending toRadio: {stripnl(toRadio)}")

            if not toRadio.HasField("packet"):
                # not a mesh packet -- send immediately, give queue a chance,
                # this makes heartbeat trigger queue
                self._sendToRadioImpl(toRadio)
            else:
                # mesh packet -- queue
                self.queue[toRadio.packet.id] = toRadio

            resent_queue = collections.OrderedDict()

            while self.queue:
                # logging.warn("queue: " + " ".join(f'{k:08x}' for k in self.queue))
                while not self._queueHasFreeSpace():
                    logging.debug("Waiting for free space in TX Queue")
                    time.sleep(0.5)
                try:
                    to_resend = self.queue.popitem(last=False)
                except KeyError:
                    break
                _id, packet = to_resend
                # logging.warn(f"packet: {packetId:08x} {packet}")
                resent_queue[_id] = packet
                if packet is False:
                    continue
                self._queueClaim()
                if packet != toRadio:
                    logging.debug(f"Resending packet ID {_id:08x} {packet}")
                self._sendToRadioImpl(packet)

            # logging.warn("resentQueue: " + " ".join(f'{k:08x}' for k in resentQueue))
            for _id, packet in resent_queue.items():
                if (
                        self.queue.pop(_id, False) is False
                ):  # Packet got acked under us
                    logging.debug(f"packet {_id:08x} got acked under us")
                    continue
                if packet:
                    self.queue[_id] = packet
            # logging.warn("queue + resentQueue: " + " ".join(f'{k:08x}' for k in self.queue))

    def _sendToRadioImpl(self, toRadio: mesh_pb2.ToRadio) -> None:
        """Send a ToRadio protobuf to the device"""
        logging.error(f"Subclass must provide toradio: {toRadio}")

    def _handleConfigComplete(self) -> None:
        """
        Done with initial config messages, now send regular MeshPackets
        to ask for settings and channels
        """
        self.localNode.setChannels(self.channels)

        # the following should only be called after we have settings and channels
        self._connected()  # Tell everyone else we are ready to go

    def _handleQueueStatusFromRadio(self, queueStatus) -> None:
        self.queueStatus = queueStatus
        logging.debug(
            f"TX QUEUE free {queueStatus.free} of {queueStatus.maxlen}," 
            f"res = ({queueStatus.res}, id) = {queueStatus.mesh_packet_id:08x} "
        )

        if queueStatus.res:
            return

        # logging.warn("queue: " + " ".join(f'{k:08x}' for k in self.queue))
        just_queued = self.queue.pop(queueStatus.mesh_packet_id, None)

        if just_queued is None and queueStatus.mesh_packet_id != 0:
            self.queue[queueStatus.mesh_packet_id] = False
            logging.debug(
                f"Reply for unexpected packet ID {queueStatus.mesh_packet_id:08x}"
            )

    def _handleFromRadio(self, fromRadioBytes):
        """
        Handle a packet that arrived from the radio
        (update model and publish events) called by subclasses
        """
        _key = None
        _from_radio = mesh_pb2.FromRadio()
        _from_radio.ParseFromString(fromRadioBytes)
        _message = google.protobuf.json_format.MessageToDict(_from_radio)
        _keys = list(_message.keys())
        if len(_keys) == 1:
            _key = _keys[0]
        else:
            raise ValueError(f"Something is wrong with the message, {','.join(_keys)}")
        logging.debug(f"Received {_key} message")
        if _key == "myInfo":
            self.my_node_info = MyNodeInfo(**_message["myInfo"])
        elif _key == "metadata" in _message:
            self.metadata = DeviceMetadata(**_message["metadata"])
        elif "nodeInfo" in _message:
            _node_info = NodeInfo(**_message["nodeInfo"])
            self.nodes[_node_info.num] = _node_info
            logging.debug(f"Got {len(list(self.nodes.keys()))} nodes")
            publishingThread.queueWork(
                lambda: pub.sendMessage(
                    "meshtastic.node.updated", node=_node_info.dict(), interface=self
                )
            )
        elif "channel" in _message:
            _channel = Channel(**_message["channel"])
            self.channels[_channel.index] = _channel
            logging.debug(f"Setting channel {_channel.index}")

        elif "config" in _message:
            self.config.update(**_message["config"])

        elif "moduleConfig" in _message:
            self.module_config.update(**_message["moduleConfig"])

        elif _from_radio.config_complete_id == self.configId:
            # we ignore the config_complete_id, it is unneeded for our
            # stream API fromRadio.config_complete_id
            logging.debug(f"Config complete ID {self.configId}")
            self._handleConfigComplete()

        elif _from_radio.HasField("rebooted") and _from_radio.rebooted:
            # Tell clients the device went away.  Careful not to call the overridden
            # subclass version that closes the serial port
            MeshInterface._disconnected(self)

            self._startConfig()  # redownload the node db etc...
        else:
            logging.warning(F"Unhandled message {_key}")
        return None

    def _nodeNumToId(self, num):
        """Map a node node number to a node ID

        Arguments:
            num {int} -- Node number

        Returns:
            string -- Node ID
        """
        if num == BROADCAST_NUM:
            return BROADCAST_ADDR

        try:
            return self.nodesByNum[num]["user"]["id"]
        except:
            logging.debug(f"Node {num} not found for fromId")
            return None

    def _getOrCreateByNum(self, nodeNum):
        """Given a nodenum find the NodeInfo in the DB (or create if necessary)"""
        if nodeNum == BROADCAST_NUM:
            raise MeshInterface.MeshInterfaceError("Can not create/find nodenum by the broadcast num")

        if nodeNum in self.nodesByNum:
            return self.nodesByNum[nodeNum]
        else:
            n = {"num": nodeNum}  # Create a minimal node db entry
            self.nodesByNum[nodeNum] = n
            return n

    def _handleChannel(self, channel):
        """During initial config the local node will proactively send all N (8) channels it knows"""
        self._localChannels.append(channel)

    def _handlePacketFromRadio(self, meshPacket, hack=False):
        """Handle a MeshPacket that just arrived from the radio

        hack - well, since we used 'from', which is a python keyword,
               as an attribute to MeshPacket in protobufs,
               there really is no way to do something like this:
                    meshPacket = mesh_pb2.MeshPacket()
                    meshPacket.from = 123
               If hack is True, we can unit test this code.

        Will publish one of the following events:
        - meshtastic.receive.text(packet = MeshPacket dictionary)
        - meshtastic.receive.position(packet = MeshPacket dictionary)
        - meshtastic.receive.user(packet = MeshPacket dictionary)
        - meshtastic.receive.data(packet = MeshPacket dictionary)
        """
        asDict = google.protobuf.json_format.MessageToDict(meshPacket)

        # We normally decompose the payload into a dictionary so that the client
        # doesn't need to understand protobufs.  But advanced clients might
        # want the raw protobuf, so we provide it in "raw"
        asDict["raw"] = meshPacket

        # from might be missing if the nodenum was zero.
        if not hack and "from" not in asDict:
            asDict["from"] = 0
            logging.error(
                f"Device returned a packet we sent, ignoring: {stripnl(asDict)}"
            )
            print(
                f"Error: Device returned a packet we sent, ignoring: {stripnl(asDict)}"
            )
            return
        if "to" not in asDict:
            asDict["to"] = 0

        # /add fromId and toId fields based on the node ID
        try:
            asDict["fromId"] = self._nodeNumToId(asDict["from"])
        except Exception as ex:
            logging.warning(f"Not populating fromId {ex}")
        try:
            asDict["toId"] = self._nodeNumToId(asDict["to"])
        except Exception as ex:
            logging.warning(f"Not populating toId {ex}")

        # We could provide our objects as DotMaps - which work with . notation or as dictionaries
        # asObj = DotMap(asDict)
        topic = "meshtastic.receive"  # Generic unknown packet type

        decoded = None
        port_number = portnums_pb2.PortNum.Name(portnums_pb2.PortNum.UNKNOWN_APP)
        if "decoded" in asDict:
            decoded = asDict["decoded"]
            # The default MessageToDict converts byte arrays into base64 strings.
            # We don't want that - it messes up data payload.  So slam in the correct
            # byte array.
            decoded["payload"] = meshPacket.decoded.payload

            # UNKNOWN_APP is the default protobuf portnum value, and therefore if not
            # set it will not be populated at all to make API usage easier, set
            # it to prevent confusion
            if "portnum" not in decoded:
                decoded["portnum"] = port_number
                logging.warning(f"portnum was not in decoded. Setting to:{port_number}")
            else:
                port_number = decoded["portnum"]

            topic = f"meshtastic.receive.data.{port_number}"

            # decode position protobufs and update nodedb, provide decoded version
            # as "position" in the published msg move the following into a 'decoders'
            # API that clients could register?
            portNumInt = meshPacket.decoded.portnum  # we want portnum as an int
            handler = protocols.get(portNumInt)
            # The decoded protobuf as a dictionary (if we understand this message)
            p = None
            if handler is not None:
                topic = f"meshtastic.receive.{handler.name}"

                # Convert to protobuf if possible
                if handler.protobufFactory is not None:
                    pb = handler.protobufFactory()
                    pb.ParseFromString(meshPacket.decoded.payload)
                    p = google.protobuf.json_format.MessageToDict(pb)
                    asDict["decoded"][handler.name] = p
                    # Also provide the protobuf raw
                    asDict["decoded"][handler.name]["raw"] = pb

                # Call specialized onReceive if necessary
                if handler.onReceive is not None:
                    handler.onReceive(self, asDict)

            # Is this message in response to a request, if so, look for a handler
            requestId = decoded.get("requestId")
            if requestId is not None:
                logging.debug(f"Got a response for requestId {requestId}")
                # We ignore ACK packets, but send NAKs and data responses to the handlers
                routing = decoded.get("routing")
                isAck = routing is not None and ("errorReason" not in routing or routing["errorReason"] == "NONE")
                if not isAck:
                    # we keep the responseHandler in dict until we get a non ack
                    handler = self.responseHandlers.pop(requestId, None)
                    if handler is not None:
                        if not isAck or (isAck and handler.__name__ == "onAckNak"):
                            logging.debug(f"Calling response handler for requestId {requestId}")
                            handler.callback(asDict)

        logging.debug(f"Publishing {topic}: packet={stripnl(asDict)} ")
        publishingThread.queueWork(
            lambda: pub.sendMessage(topic, packet=asDict, interface=self)
        )
