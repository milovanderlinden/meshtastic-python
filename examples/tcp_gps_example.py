"""Demonstration of how to look up a radio's location via its LAN connection.
   Before running, connect your machine to the same WiFi network as the radio.
"""

try:
    import meshtastic.tcp_interface
except ModuleNotFoundError:
    # see if we are in a development environment that does not have a compiled package
    import sys
    from pathlib import Path
    path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
    sys.path.insert(0, path)
    import meshtastic.tcp_interface


radio_hostname = "meshtastic.local"  # Can also be an IP
iface = meshtastic.tcp_interface.TCPInterface(radio_hostname)
my_node_num = iface.myInfo.my_node_num
pos = iface.nodesByNum[my_node_num]["position"]
print(pos)

iface.close()
