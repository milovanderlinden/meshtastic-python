"""Simple program to demo how to use meshtastic library.
   To run: python examples/info.py
"""

try:
    import meshtastic.serial_interface
except ModuleNotFoundError:
    # see if we are in a development environment that does not have a compiled package
    import sys
    from pathlib import Path
    path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
    sys.path.insert(0, path)
    import meshtastic.serial_interface


iface = meshtastic.serial_interface.SerialInterface()

# call showInfo() just to ensure values are populated
# info = iface.showInfo()


if iface.nodes:
    for n in iface.nodes.values():
        if n["num"] == iface.myInfo.my_node_num:
            print(n["user"]["hwModel"])
            break

iface.close()
