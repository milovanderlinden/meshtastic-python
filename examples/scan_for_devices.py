"""Program to scan for hardware
   To run: python examples/scan_for_devices.py
"""

import sys

try:
    from meshtastic.util import (
        active_ports_on_supported_devices,
        detect_supported_devices,
        get_unique_vendor_ids,
    )
except ModuleNotFoundError:
    # see if we are in a development environment that does not have a compiled package
    from pathlib import Path
    path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
    sys.path.insert(0, path)
    from meshtastic.util import (
        active_ports_on_supported_devices,
        detect_supported_devices,
        get_unique_vendor_ids,
    )


# simple arg check
if len(sys.argv) != 1:
    print(f"usage: {sys.argv[0]}")
    print("Detect which device we might have.")
    sys.exit(3)

vids = get_unique_vendor_ids()
print(f"Searching for all devices with these vendor ids {vids}")

sds = detect_supported_devices()
if len(sds) > 0:
    print("Detected possible devices:")
for d in sds:
    print(f" name:{d.name}{d.version} firmware:{d.for_firmware}")

ports = active_ports_on_supported_devices(sds)
print(f"ports:{ports}")
