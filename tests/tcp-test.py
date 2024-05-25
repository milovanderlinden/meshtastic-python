# reported by @ScriptBlock

import sys

from pubsub import pub

from meshtastic.tcp_interface import TCPInterface


def onConnection(
    interface, topic=pub.AUTO_TOPIC
):  # called when we (re)connect to the radio
    print(interface.myInfo)
    interface.close()


pub.subscribe(onConnection, "meshtastic.connection.established")
interface = TCPInterface(sys.argv[1])
