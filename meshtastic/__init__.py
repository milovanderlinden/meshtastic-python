"""
# an API for Meshtastic devices

Primary class: SerialInterface
Install with pip: "[pip3 install meshtastic](https://pypi.org/project/meshtastic/)"
Source code on [GitHub](https://github.com/meshtastic/python)

properties of SerialInterface:

- localConfig - Current radio configuration and device settings, if you write to this the new settings will be applied to
the device.
- nodes - The database of received nodes.  Includes always up-to-date location and username information for each
node in the mesh.  This is a read-only datastructure.
- nodesByNum - like "nodes" but keyed by nodeNum instead of nodeId
- myInfo - Contains read-only information about the local radio device (software version, hardware version, etc.)

# Published PubSub topics

We use a [publish-subscribe](https://pypubsub.readthedocs.io/en/v4.0.3/) model to communicate asynchronous events.
Available topics:

- meshtastic.connection.established - published once we've successfully connected to the radio and downloaded the
node DB - meshtastic.connection.lost - published once we've lost our link to the radio - meshtastic.receive.text(
packet) - delivers a received packet as a dictionary, if you only care about a particular type of packet, you should
subscribe to the full topic name.  If you want to see all packets, simply subscribe to "meshtastic.receive". -
meshtastic.receive.position(packet) - meshtastic.receive.user(packet) - meshtastic.receive.data.portnum(packet) (
where portnum is an integer or well known PortNum enum) - meshtastic.node.updated(node = NodeInfo) - published when a
node in the DB changes (appears, location changed, username changed, etc...)

We receive position, user, or data packets from the mesh.  You probably only care about meshtastic.receive.data.  The
first argument for that publish will be the packet.  Text or binary data packets (from sendData or sendText) will
both arrive this way.  If you print packet you'll see the fields in the dictionary.  decoded.data.payload will
contain the raw bytes that were sent.  If the packet was sent with sendText, decoded.data.text will **also** be
populated with the decoded string.  For ASCII these two strings will be the same, but for unicode scripts they can be
different.

# Example Usage
```
import meshtastic.serial_interface
from pubsub import pub

def onReceive(packet, interface): # called when a packet arrives
    print(f"Received: {packet}")

def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    # defaults to broadcast, specify a destination ID if you wish
    interface.sendText("hello mesh")

pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")
# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.serial_interface.SerialInterface()

```

"""
