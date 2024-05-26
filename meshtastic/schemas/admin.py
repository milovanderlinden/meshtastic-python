from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from .channel import Channel
from .config import Config
from .mesh import User, Position, NodeRemoteHardwarePin, DeviceMetadata
from .module_config import ModuleConfig
from .connection_status import DeviceConnectionStatus


class HamParameters(BaseModel):
    """
    # proto source: admin.proto
    message: HamParameters

    https://github.com/meshtastic/protobufs/blob/master/meshtastic/admin.proto#L351

    """
    call_sign: Optional[str] = Field(default=None)
    tx_power: Optional[int] = Field(default=None)
    frequency: Optional[float] = Field(default=None)
    short_name: Optional[str] = Field(default=None)


class NodeRemoteHardwarePinsResponse(BaseModel):
    """
    proto source: admin.proto
    message: NodeRemoteHardwarePinsResponse

    https://github.com/meshtastic/protobufs/blob/master/meshtastic/admin.proto#L231
    """
    node_remote_hardware_pins: Optional[List[NodeRemoteHardwarePin]] = Field(default=None)


class AdminMessage(BaseModel):
    """
    proto source: admin.proto
    message: AdminMessage

    https://github.com/meshtastic/protobufs/blob/master/meshtastic/admin.proto#L22
    """
    class ConfigType(str, Enum):
        DEVICE_CONFIG = 'DEVICE_CONFIG'
        POSITION_CONFIG = 'POSITION_CONFIG'
        POWER_CONFIG = 'POWER_CONFIG'
        NETWORK_CONFIG = 'NETWORK_CONFIG'
        DISPLAY_CONFIG = 'DISPLAY_CONFIG'
        LORA_CONFIG = 'LORA_CONFIG'
        BLUETOOTH_CONFIG = 'BLUETOOTH_CONFIG'

    class ModuleConfigType(str, Enum):
        MQTT_CONFIG = 'MQTT_CONFIG'
        SERIAL_CONFIG = 'SERIAL_CONFIG'
        EXTNOTIF_CONFIG = 'EXTNOTIF_CONFIG'
        STOREFORWARD_CONFIG = 'STOREFORWARD_CONFIG'
        RANGETEST_CONFIG = 'RANGETEST_CONFIG'
        TELEMETRY_CONFIG = 'TELEMETRY_CONFIG'
        CANNEDMSG_CONFIG = 'CANNEDMSG_CONFIG'
        AUDIO_CONFIG = 'AUDIO_CONFIG'
        REMOTEHARDWARE_CONFIG = 'REMOTEHARDWARE_CONFIG'
        NEIGHBORINFO_CONFIG = 'NEIGHBORINFO_CONFIG'
        AMBIENTLIGHTING_CONFIG = 'AMBIENTLIGHTING_CONFIG'
        DETECTIONSENSOR_CONFIG = 'DETECTIONSENSOR_CONFIG'
        PAXCOUNTER_CONFIG = 'PAXCOUNTER_CONFIG'

    get_channel_request: Optional[int] = Field(default=None)
    get_channel_response: Optional[Channel] = Field(default=None)
    get_owner_request: Optional[bool] = Field(default=None)
    get_owner_response: Optional[User] = Field(default=None)
    get_config_request: Optional[ConfigType] = Field(default=None)
    get_config_response: Optional[ModuleConfig] = Field(default=None)
    get_module_config_request: Optional[ModuleConfigType] = Field(default=None)
    get_module_config_response: Optional[ModuleConfig] = Field(default=None)
    get_canned_message_module_messages_request: Optional[bool] = Field(default=None)
    get_canned_message_module_messages_response: Optional[str] = Field(default=None)
    get_device_metadata_request: Optional[bool] = Field(default=None)
    get_device_metadata_response: Optional[DeviceMetadata] = Field(default=None)
    get_ringtone_request: Optional[bool] = Field(default=None)
    get_ringtone_response: Optional[str] = Field(default=None)
    get_device_connection_status_request: Optional[bool] = Field(default=None)
    get_device_connection_status_response: Optional[DeviceConnectionStatus] = Field(default=None)
    set_ham_mode: Optional[HamParameters] = Field(default=None)
    get_node_remote_hardware_pins_request: Optional[bool] = Field(default=None)
    get_node_remote_hardware_pins_response: Optional[NodeRemoteHardwarePinsResponse] = Field(default=None)
    enter_dfu_mode_request: Optional[bool] = Field(default=None)
    delete_file_request: Optional[bool] = Field(default=None)
    set_owner: Optional[User] = Field(default=None)
    set_channel: Optional[Channel] = Field(default=None)
    set_config: Optional[Config] = Field(default=None)
    set_module_config: Optional[ModuleConfig] = Field(default=None)
    set_canned_message_module_messages: Optional[str] = Field(default=None)
    set_ringtone_message: Optional[str] = Field(default=None)
    remove_by_nodenum: Optional[int] = Field(default=None)
    set_favorite_node: Optional[int] = Field(default=None)
    remove_favorite_node: Optional[int] = Field(default=None)
    set_fixed_position: Optional[Position] = Field(default=None)
    remove_fixed_position: Optional[bool] = Field(default=None)
    begin_edit_settings: Optional[bool] = Field(default=None)
    commit_edit_settings: Optional[bool] = Field(default=None)
    reboot_ota_seconds: Optional[int] = Field(default=None)
    exit_simulator: Optional[bool] = Field(default=None)
    reboot_seconds: Optional[int] = Field(default=None)
    shutdown_seconds: Optional[int] = Field(default=None)
    factory_reset: Optional[int] = Field(default=None)
    nodedb_reset: Optional[int] = Field(default=None)
