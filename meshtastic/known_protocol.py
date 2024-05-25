import logging
from typing import NamedTuple, Optional, Callable

from . import (
    portnums_pb2,
    mesh_pb2,
    admin_pb2,
    telemetry_pb2,
    remote_hardware_pb2,
    paxcount_pb2,
    storeforward_pb2,
    mqtt_pb2
)


class KnownProtocol(NamedTuple):
    """Used to automatically decode known protocol payloads"""

    name: str
    # portnum: int, now a key
    # If set, will be called to phrase as a protocol buffer
    protobufFactory: Optional[Callable] = None
    # If set, invoked as onReceive(interface, packet)
    onReceive: Optional[Callable] = None


def _onTextReceive(iface, asDict):
    """Special text auto parsing for received messages"""
    # We don't throw if the utf8 is invalid in the text message.  Instead we just don't populate
    # the decoded.data.text and we log an error message.  This at least allows some delivery to
    # the app and the app can deal with the missing decoded representation.
    #
    # Usually btw this problem is caused by apps sending binary data but setting the payload type to
    # text.
    logging.debug(f"in _onTextReceive() asDict:{asDict}")
    try:
        asBytes = asDict["decoded"]["payload"]
        asDict["decoded"]["text"] = asBytes.decode("utf-8")
    except Exception as ex:
        logging.error(f"Malformatted utf8 in text message: {ex}")
    _receiveInfoUpdate(iface, asDict)


def _onPositionReceive(iface, asDict):
    """Special auto parsing for received messages"""
    logging.debug(f"in _onPositionReceive() asDict:{asDict}")
    if "decoded" in asDict:
        if "position" in asDict["decoded"] and "from" in asDict:
            p = asDict["decoded"]["position"]
            logging.debug(f"p:{p}")
            p = iface._fixupPosition(p)
            logging.debug(f"after fixup p:{p}")
            # update node DB as needed
            iface._getOrCreateByNum(asDict["from"])["position"] = p


def _onNodeInfoReceive(iface, asDict):
    """Special auto parsing for received messages"""
    logging.debug(f"in _onNodeInfoReceive() asDict:{asDict}")
    if "decoded" in asDict:
        if "user" in asDict["decoded"] and "from" in asDict:
            p = asDict["decoded"]["user"]
            # decode user protobufs and update nodedb, provide decoded version as "position" in the published msg
            # update node DB as needed
            n = iface._getOrCreateByNum(asDict["from"])
            n["user"] = p
            # We now have a node ID, make sure it is up-to-date in that table
            iface.nodes[p["id"]] = n
            _receiveInfoUpdate(iface, asDict)


def _receiveInfoUpdate(iface, asDict):
    if "from" in asDict:
        iface._getOrCreateByNum(asDict["from"])["lastReceived"] = asDict
        iface._getOrCreateByNum(asDict["from"])["lastHeard"] = asDict.get("rxTime")
        iface._getOrCreateByNum(asDict["from"])["snr"] = asDict.get("rxSnr")
        iface._getOrCreateByNum(asDict["from"])["hopLimit"] = asDict.get("hopLimit")


"""Well known message payloads can register decoders for automatic protobuf parsing"""
protocols = {
    portnums_pb2.PortNum.TEXT_MESSAGE_APP: KnownProtocol(
        "text", onReceive=_onTextReceive
    ),
    portnums_pb2.PortNum.RANGE_TEST_APP: KnownProtocol(
        "rangetest", onReceive=_onTextReceive
    ),
    portnums_pb2.PortNum.DETECTION_SENSOR_APP: KnownProtocol(
        "detectionsensor", onReceive=_onTextReceive
    ),

    portnums_pb2.PortNum.POSITION_APP: KnownProtocol(
        "position", mesh_pb2.Position, _onPositionReceive
    ),
    portnums_pb2.PortNum.NODEINFO_APP: KnownProtocol(
        "user", mesh_pb2.User, _onNodeInfoReceive
    ),
    portnums_pb2.PortNum.ADMIN_APP: KnownProtocol("admin", admin_pb2.AdminMessage),
    portnums_pb2.PortNum.ROUTING_APP: KnownProtocol("routing", mesh_pb2.Routing),
    portnums_pb2.PortNum.TELEMETRY_APP: KnownProtocol(
        "telemetry", telemetry_pb2.Telemetry
    ),
    portnums_pb2.PortNum.REMOTE_HARDWARE_APP: KnownProtocol(
        "remotehw", remote_hardware_pb2.HardwareMessage
    ),
    portnums_pb2.PortNum.SIMULATOR_APP: KnownProtocol("simulator", mesh_pb2.Compressed),
    portnums_pb2.PortNum.TRACEROUTE_APP: KnownProtocol(
        "traceroute", mesh_pb2.RouteDiscovery
    ),
    portnums_pb2.PortNum.WAYPOINT_APP: KnownProtocol("waypoint", mesh_pb2.Waypoint),
    portnums_pb2.PortNum.PAXCOUNTER_APP: KnownProtocol("paxcounter", paxcount_pb2.Paxcount),
    portnums_pb2.PortNum.STORE_FORWARD_APP: KnownProtocol("storeforward", storeforward_pb2.StoreAndForward),
    portnums_pb2.PortNum.NEIGHBORINFO_APP: KnownProtocol("neighborinfo", mesh_pb2.NeighborInfo),
    portnums_pb2.PortNum.MAP_REPORT_APP: KnownProtocol("mapreport", mqtt_pb2.MapReport),
}
