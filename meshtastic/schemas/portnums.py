from enum import IntEnum


class PortNum(IntEnum):
    """
    proto source: portnums.proto
    enum: PortNum
    """
    UNKNOWN_APP = 0
    TEXT_MESSAGE_APP = 1
    REMOTE_HARDWARE_APP = 2
    POSITION_APP = 3
    NODEINFO_APP = 4
    ROUTING_APP = 5
    ADMIN_APP = 6
    TEXT_MESSAGE_COMPRESSED_APP = 7
    WAYPOINT_APP = 8
    AUDIO_APP = 9
    DETECTION_SENSOR_APP = 10
    REPLY_APP = 32
    IP_TUNNEL_APP = 33
    PAXCOUNTER_APP = 34
    SERIAL_APP = 64
    STORE_FORWARD_APP = 65
    RANGE_TEST_APP = 66
    TELEMETRY_APP = 67
    ZPS_APP = 68
    SIMULATOR_APP = 69
    TRACEROUTE_APP = 70
    NEIGHBORINFO_APP = 71
    ATAK_PLUGIN = 72
    MAP_REPORT_APP = 73
    PRIVATE_APP = 256
    ATAK_FORWARDER = 257
    MAX = 511
