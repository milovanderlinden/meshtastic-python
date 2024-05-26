from enum import IntEnum
from typing import Optional, List

from pydantic import BaseModel, Field

from .channel import Channel
from .config import Config
from .module_config import ModuleConfig


class HamParameters(BaseModel):
    """
    module: admin.proto
    message: HamParameters
    """
    call_sign: Optional[str] = Field(default=None)
    tx_power: Optional[int] = Field(default=None)
    frequency: Optional[float] = Field(default=None)
    short_name: Optional[str] = Field(default=None)


class NodeRemoteHardwarePinsResponse(BaseModel):
    """
    module: admin.proto
    message: NodeRemoteHardwarePinsResponse
    """
    node_remote_hardware_pins: Optional[List[NodeRemoteHardwarePin]] = Field(default=None)


class AdminMessage(BaseModel):
    """
    module: admin.proto
    message: AdminMessage
    """
    class ConfigType(IntEnum):
        DEVICE_CONFIG = 0
        POSITION_CONFIG = 1
        POWER_CONFIG = 2
        NETWORK_CONFIG = 3
        DISPLAY_CONFIG = 4
        LORA_CONFIG = 5
        BLUETOOTH_CONFIG = 6

    class ModuleConfigType(IntEnum):
        MQTT_CONFIG = 0
        SERIAL_CONFIG = 1
        EXTNOTIF_CONFIG = 2
        STOREFORWARD_CONFIG = 3
        RANGETEST_CONFIG = 4
        TELEMETRY_CONFIG = 5
        CANNEDMSG_CONFIG = 6
        AUDIO_CONFIG = 7
        REMOTEHARDWARE_CONFIG = 8
        NEIGHBORINFO_CONFIG = 9
        AMBIENTLIGHTING_CONFIG = 10
        DETECTIONSENSOR_CONFIG = 11
        PAXCOUNTER_CONFIG = 12

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
