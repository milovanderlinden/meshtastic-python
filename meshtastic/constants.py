# Note: To follow PEP224, comments should be after the module variable.
from .util import DeferredExecution

LOCAL_ADDR = "^local"
"""A special ID that means the local node"""

BROADCAST_NUM = 0xFFFFFFFF
"""if using 8 bit nodenums this will be shortened on the target"""

BROADCAST_ADDR = "^all"
"""A special ID that means broadcast"""

OUR_APP_VERSION = 20300
"""The numeric buildnumber (shared with android apps) specifying the
   level of device code we are guaranteed to understand

   format is Mmmss (where M is 1+the numeric major number. i.e. 20120 means 1.1.20
"""

publishingThread = DeferredExecution("publishing")
