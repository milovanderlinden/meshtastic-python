"""Simple program to show serial ports.
"""

import sys

try:
    from meshtastic.util import findPorts
except ModuleNotFoundError:
    # see if we are in a development environment that does not have a compiled package
    from pathlib import Path
    path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
    sys.path.insert(0, path)
    from meshtastic.util import findPorts


print(findPorts())
