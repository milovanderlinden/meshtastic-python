import base64
import re
from datetime import datetime
from enum import IntEnum, Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, field_validator, model_validator
from .channel import Channel
from .config import Config, Role
from .module_config import ModuleConfig, RemoteHardwarePin
from .portnums import PortNum
from .telemetry import DeviceMetrics
from .xmodem import XModem


class HardwareModel(str, Enum):
    """
    proto source: mesh.proto
    message: HardwareModel
    """
    UNSET = 'UNSET'
    TLORA_V2 = 'TLORA_V2'
    TLORA_V1 = 'TLORA_V1'
    TLORA_V2_1_1P6 = 'TLORA_V2_1_1P6'
    TBEAM = 'TBEAM'
    HELTEC_V2_0 = 'HELTEC_V2_0'
    TBEAM_V0P7 = 'TBEAM_V0P7'
    T_ECHO = 'T_ECHO'
    TLORA_V1_1P3 = 'TLORA_V1_1P3'
    RAK4631 = 'RAK4631'
    HELTEC_V2_1 = 'HELTEC_V2_1'
    HELTEC_V1 = 'HELTEC_V1'
    LILYGO_TBEAM_S3_CORE = 'LILYGO_TBEAM_S3_CORE'
    RAK11200 = 'RAK11200'
    NANO_G1 = 'NANO_G1'
    TLORA_V2_1_1P8 = 'TLORA_V2_1_1P8'
    TLORA_T3_S3 = 'TLORA_T3_S3'
    NANO_G1_EXPLORER = 'NANO_G1_EXPLORER'
    NANO_G2_ULTRA = 'NANO_G2_ULTRA'
    LORA_TYPE = 'LORA_TYPE'
    WIPHONE = 'WIPHONE'
    STATION_G1 = 'STATION_G1'
    RAK11310 = 'RAK11310'
    SENSELORA_RP2040 = 'SENSELORA_RP2040'
    SENSELORA_S3 = 'SENSELORA_S3'
    CANARYONE = 'CANARYONE'
    RP2040_LORA = 'RP2040_LORA'
    STATION_G2 = 'STATION_G2'
    LORA_RELAY_V1 = 'LORA_RELAY_V1'
    NRF52840DK = 'NRF52840DK'
    PPR = 'PPR'
    GENIEBLOCKS = 'GENIEBLOCKS'
    NRF52_UNKNOWN = 'NRF52_UNKNOWN'
    PORTDUINO = 'PORTDUINO'
    ANDROID_SIM = 'ANDROID_SIM'
    DIY_V1 = 'DIY_V1'
    NRF52840_PCA10059 = 'NRF52840_PCA10059'
    DR_DEV = 'DR_DEV'
    M5STACK = 'M5STACK'
    HELTEC_V3 = 'HELTEC_V3'
    HELTEC_WSL_V3 = 'HELTEC_WSL_V3'
    BETAFPV_2400_TX = 'BETAFPV_2400_TX'
    BETAFPV_900_NANO_TX = 'BETAFPV_900_NANO_TX'
    RPI_PICO = 'RPI_PICO'
    HELTEC_WIRELESS_TRACKER = 'HELTEC_WIRELESS_TRACKER'
    HELTEC_WIRELESS_PAPER = 'HELTEC_WIRELESS_PAPER'
    T_DECK = 'T_DECK'
    T_WATCH_S3 = 'T_WATCH_S3'
    PICOMPUTER_S3 = 'PICOMPUTER_S3'
    HELTEC_HT62 = 'HELTEC_HT62'
    EBYTE_ESP32_S3 = 'EBYTE_ESP32_S3'
    ESP32_S3_PICO = 'ESP32_S3_PICO'
    CHATTER_2 = 'CHATTER_2'
    HELTEC_WIRELESS_PAPER_V1_0 = 'HELTEC_WIRELESS_PAPER_V1_0'
    HELTEC_WIRELESS_TRACKER_V1_0 = 'HELTEC_WIRELESS_TRACKER_V1_0'
    UNPHONE = 'UNPHONE'
    TD_LORAC = 'TD_LORAC'
    CDEBYTE_EORA_S3 = 'CDEBYTE_EORA_S3'
    TWC_MESH_V4 = 'TWC_MESH_V4'
    NRF52_PROMICRO_DIY = 'NRF52_PROMICRO_DIY'
    RADIOMASTER_900_BANDIT_NANO = 'RADIOMASTER_900_BANDIT_NANO'
    PRIVATE_HW = 'PRIVATE_HW'


class LocSource(IntEnum):
    """
    proto source: mesh.proto
    enum: Position.LocSource
    """
    LOC_UNSET = 0
    LOC_MANUAL = 1
    LOC_INTERNAL = 2
    LOC_EXTERNAL = 3


class AltSource(IntEnum):
    """
    proto source: mesh.proto
    enum: Position.AltSource
    """
    ALT_UNSET = 0
    ALT_MANUAL = 1
    ALT_INTERNAL = 2
    ALT_EXTERNAL = 3
    ALT_BAROMETRIC = 4


class Position(BaseModel):
    """
    proto source: mesh.proto
    message: Position
    """
    # payload
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    altitude: Optional[int] = Field(default=None)
    time: Optional[datetime] = Field(default=None)
    location_source: Optional[LocSource] = Field(default=None)
    altitude_source: Optional[AltSource] = Field(default=None)
    timestamp: Optional[int] = Field(default=None)
    timestamp_millis_adjust: Optional[int] = Field(default=None)
    altitude_hae: Optional[int] = Field(default=None)
    altitude_geoidal_separation: Optional[int] = Field(default=None)
    PDOP: Optional[int] = Field(default=None)
    HDOP: Optional[int] = Field(default=None)
    VDOP: Optional[int] = Field(default=None)
    gps_accuracy: Optional[int] = Field(default=None)
    ground_speed: Optional[int] = Field(default=None)
    ground_track: Optional[int] = Field(default=None)
    fix_quality: Optional[int] = Field(default=None)
    fix_type: Optional[int] = Field(default=None)
    sats_in_view: Optional[int] = Field(default=None)
    sensor_id: Optional[int] = Field(default=None)
    next_update: Optional[int] = Field(default=None)
    seq_number: Optional[int] = Field(default=None)
    precision_bits: Optional[int] = Field(default=None)

    @model_validator(mode='before')
    @classmethod
    def i_preprocess_validator(cls, values: Dict[str, Any]):
        """
        The model validator allows to set longitude, latitude to floats
        and time to a datetime object
        """
        if "longitudeI" in values:
            values['longitude'] = values['longitudeI'] * 1e-7
        if "latitudeI" in values:
            values['latitude'] = values['latitudeI'] * 1e-7
        if "time" in values:
            values['time'] = datetime.fromtimestamp(values["time"])
        return values


class User(BaseModel):
    """
    proto source: mesh.proto
    message: User
    """
    id: Optional[str] = Field(default=None)
    long_name: Optional[str] = Field(default=None, alias="longName")
    short_name: Optional[str] = Field(default=None, alias="shortName")
    macaddr: Optional[str] = Field(default=None, deprecated=True)
    hw_model: Optional[HardwareModel] = Field(default=None, alias="hwModel")
    is_licensed: Optional[bool] = Field(default=None)
    role: Optional[Role] = Field(default=None)

    @field_validator('macaddr', mode='before')
    @classmethod
    def macaddr_validator(cls, v: str):
        """
        Convert the base 64 encoded value to a mac address
        val - base64 encoded value (ex: '/c0gFyhb')
        returns: a string formatted like a mac address (ex: 'fd:cd:20:17:28:5b')
        """
        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", v):
            val_as_bytes = base64.b64decode(v)
            return ":".join(f"{x:02x}" for x in val_as_bytes)
        return v


class RouteDiscovery(BaseModel):
    """
    proto source: mesh.proto
    message: RouteDiscovery
    """
    route: Optional[List[int]] = Field(default=None)


class Error(IntEnum):
    """
    proto source: mesh.proto
    enum: Routing.Error
    """
    NONE = 0
    NO_ROUTE = 1
    GOT_NAK = 2
    TIMEOUT = 3
    NO_INTERFACE = 4
    MAX_RETRANSMIT = 5
    NO_CHANNEL = 6
    TOO_LARGE = 7
    NO_RESPONSE = 8
    DUTY_CYCLE_LIMIT = 9
    BAD_REQUEST = 32
    NOT_AUTHORIZED = 33


class Routing(BaseModel):
    """
    proto source: mesh.proto
    message: Routing
    """
    # variant
    route_request: Optional[RouteDiscovery] = Field(default=None)
    route_reply: Optional[RouteDiscovery] = Field(default=None)
    error_reason: Optional[Error] = Field(default=None)


class Data(BaseModel):
    """
    proto source: mesh.proto
    message: Data
    """
    portnum: Optional[PortNum] = Field(default=None)
    payload: Optional[bytes] = Field(default=None)
    want_response: Optional[bool] = Field(default=None)
    dest: Optional[int] = Field(default=None)
    source: Optional[int] = Field(default=None)
    request_id: Optional[int] = Field(default=None)
    emoji: Optional[int] = Field(default=None)


class Waypoint(BaseModel):
    """
    proto source: mesh.proto
    message: Waypoint
    """
    id: Optional[int] = Field(default=None)
    latitude_i: Optional[int] = Field(default=None)
    longitude_i: Optional[int] = Field(default=None)
    expire: Optional[int] = Field(default=None)
    locked_to: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    icon: Optional[int] = Field(default=None)


class MqttClientProxyMessage(BaseModel):
    """
    proto source: mesh.proto
    message: MqttClientProxyMessage
    """
    topic: Optional[str] = Field(default=None)
    data: Optional[bytes] = Field(default=None)
    text: Optional[str] = Field(default=None)
    retained: Optional[bool] = Field(default=None)


class Priority(IntEnum):
    """
    proto source: mesh.proto
    enum: MeshPacket.Priority
    """
    UNSET = 0
    MIN = 1
    BACKGROUND = 10
    DEFAULT = 64
    RELIABLE = 70
    ACK = 120
    MAX = 127


class Delayed(IntEnum):
    """
    proto source: mesh.proto
    enum: MeshPacket.Delayed
    """
    NO_DELAY = 0
    DELAYED_BROADCAST = 1
    DELAYED_DIRECT = 2


class MeshPacket(BaseModel):
    """
    proto source: mesh.proto
    message: MeshPacket
    """
    node_from: Optional[int] = Field(default=None, alias="from")
    to: Optional[int] = Field(default=None)
    channel: Optional[int] = Field(default=None)
    data: Optional[Data] = Field(default=None)
    encrypted: Optional[bytes] = Field(default=None)
    id: Optional[int] = Field(default=None)
    rx_time: Optional[int] = Field(default=None)
    rx_snr: Optional[float] = Field(default=None)
    hop_limit: Optional[int] = Field(default=None)
    want_ack: Optional[bool] = Field(default=None)
    rx_rssi: Optional[int] = Field(default=None)
    delayed: Optional[Delayed] = Field(default=None, deprecated=True)
    via_mqtt: Optional[bool] = Field(default=None)
    hop_start: Optional[int] = Field(default=None)


class Constants(IntEnum):
    """
    proto source: mesh.proto
    enum: Constants
    """
    ZERO = 0
    DATA_PAYLOAD_LEN = 1


class NodeInfo(BaseModel):
    """
    proto source: mesh.proto
    message: NodeInfo

    """
    num: Optional[int] = Field(default=None)
    user: Optional[User] = Field(default=None)
    position: Optional[Position] = Field(default=None)
    snr: Optional[float] = Field(default=None)
    last_heard: Optional[int] = Field(default=None, alias="lastHeard")
    device_metrics: Optional[DeviceMetrics] = Field(default=None, alias="deviceMetrics")
    channel: Optional[int] = Field(default=None)
    via_mqtt: Optional[bool] = Field(default=None)
    hops_away: Optional[int] = Field(default=None)
    is_favorite: Optional[bool] = Field(default=None, alias="isFavorite")


class CriticalErrorCode(IntEnum):
    """
    proto source: mesh.proto
    enum: CriticalErrorCode
    """
    NONE = 0
    TX_WATCHDOG = 1
    SLEEP_ENTER_WAIT = 2
    NO_RADIO = 3
    UNSPECIFIED = 4
    UBLOX_UNIT_FAILED = 5
    NO_AXP192 = 6
    INVALID_RADIO_SETTING = 7
    TRANSMIT_FAILED = 8
    BROWNOUT = 9
    SX1262_FAILURE = 10
    RADIO_SPI_BUG = 11


class MyNodeInfo(BaseModel):
    """
    proto source: mesh.proto
    message: MyNodeInfo
    """
    my_node_num: Optional[int] = Field(default=None, alias="myNodeNum")
    reboot_count: Optional[int] = Field(default=None, alias="rebootCount")
    min_app_version: Optional[int] = Field(default=None, alias="minAppVersion")


class Level(IntEnum):
    """
    proto source: mesh.proto
    message: LogRecord.Level
    """
    UNSET = 0
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    TRACE = 5


class LogRecord(BaseModel):
    """
    proto source: mesh.proto
    message: LogRecord
    """
    message: Optional[str] = Field(default=None)
    time: Optional[int] = Field(default=None)
    source: Optional[str] = Field(default=None)
    level: Optional[Level] = Field(default=None)


class QueueStatus(BaseModel):
    """
    proto source: mesh.proto
    message: QueueStatus
    """
    res: Optional[int] = Field(default=None)
    free: Optional[int] = Field(default=None)
    maxlen: Optional[int] = Field(default=None)
    mesh_packet_id: Optional[int] = Field(default=None)


class Heartbeat(BaseModel):
    """
    proto source: mesh.proto
    message: Heartbeat
    """


class DeviceMetadata(BaseModel):
    """
    proto source: mesh.proto
    message: Neighbor
    """
    firmware_version: Optional[str] = Field(default=None, alias="firmwareVersion")
    device_state_version: Optional[int] = Field(default=None, alias='deviceStateVersion')
    canShutdown: Optional[bool] = Field(default=None)
    hasWifi: Optional[bool] = Field(default=None)
    hasBluetooth: Optional[bool] = Field(default=None)
    role: Optional[Role] = Field(default=None)
    position_flags: Optional[int] = Field(default=None, alias='positionFlags')
    hw_model: Optional[str] = Field(default=None, alias='hwModel')
    hasRemoteHardware: Optional[bool] = Field(default=None)


class FromRadio(BaseModel):
    """
    proto source: mesh.proto
    message: FromRadio
    """

    # oneof payload_variant
    packet: Optional[MeshPacket] = Field(default=None)
    my_info: Optional[MyNodeInfo] = Field(default=None)
    node_info: Optional[NodeInfo] = Field(default=None)
    config: Optional[Config] = Field(default=None)
    log_record: Optional[LogRecord] = Field(default=None)
    config_complete_id: Optional[int] = Field(default=None)
    rebooted: Optional[bool] = Field(default=None)
    moduleConfig: Optional[ModuleConfig] = Field(default=None)
    channel: Optional[Channel] = Field(default=None)
    queueStatus: Optional[QueueStatus] = Field(default=None)
    xmodemPacket: Optional[XModem] = Field(default=None)
    metadata: Optional[DeviceMetadata] = Field(default=None)
    mqttClientProxyMessage: Optional[MqttClientProxyMessage] = Field(default=None)


class ToRadio(BaseModel):
    """
    proto source: mesh.proto
    message: ToRadio
    """

    # oneof payload_variant
    packet: Optional[MeshPacket] = Field(default=None)
    want_config_id: Optional[int] = Field(default=None)
    disconnect: Optional[bool] = Field(default=None)
    xmodemPacket: Optional[XModem] = Field(default=None)
    mqttClientProxyMessage: Optional[MqttClientProxyMessage] = Field(default=None)
    heartbeat: Optional[Heartbeat] = Field(default=None)


class Compressed(BaseModel):
    """
    proto source: mesh.proto
    message: Compressed
    """
    portnum: Optional[PortNum] = Field(default=None)
    data: Optional[bytes] = Field(default=None)


class Neighbor(BaseModel):
    """
    proto source: mesh.proto
    message: Neighbor
    """
    node_id: Optional[int] = Field(default=None)
    snr: Optional[float] = Field(default=None)
    last_rx_time: Optional[int] = Field(default=None)
    node_broadcast_interval_secs: Optional[int] = Field(default=None)


class NeighborInfo(BaseModel):
    """
    proto source: mesh.proto
    message: NeighborInfo
    """
    node_id: Optional[int] = Field(default=None)
    last_sent_by_id: Optional[int] = Field(default=None)
    node_broadcast_interval_secs: Optional[int] = Field(default=None)
    neighbors: Optional[List[Neighbor]] = Field(default=None)


class NodeRemoteHardwarePin(BaseModel):
    """
    proto source: mesh.proto
    message: NodeRemoteHardwarePin
    """
    node_num: Optional[int] = Field(default=None)
    pin: Optional[RemoteHardwarePin] = Field(default=None)
