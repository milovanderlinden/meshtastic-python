from typing import Optional

from pydantic import BaseModel, Field

from .config import Config
from .module_config import ModuleConfig


class LocalConfig(BaseModel):
    """
    module: localonly.proto
    message: LocalConfig
    """
    device: Optional[Config.DeviceConfig] = Field(default=None)
    position: Optional[Config.PositionConfig] = Field(default=None)
    power: Optional[Config.PowerConfig] = Field(default=None)
    network: Optional[Config.NetworkConfig] = Field(default=None)
    display: Optional[Config.DisplayConfig] = Field(default=None)
    lora: Optional[Config.LoRaConfig] = Field(default=None)
    bluetooth: Optional[Config.BluetoothConfig] = Field(default=None)
    version: Optional[int] = Field(default=None)


class LocalModuleConfig(BaseModel):
    """
    module: localonly.proto
    message: LocalModuleConfig
    """
    mqtt: Optional[ModuleConfig.MQTTConfig] = Field(default=None)
    serial: Optional[ModuleConfig.SerialConfig] = Field(default=None)
    external_notification: Optional[ModuleConfig.ExternalNotificationConfig] = Field(default=None)
    store_forward: Optional[ModuleConfig.StoreForwardConfig] = Field(default=None)
    range_test: Optional[ModuleConfig.RangeTestConfig] = Field(default=None)
    telemetry: Optional[ModuleConfig.TelemetryConfig] = Field(default=None)
    canned_message: Optional[ModuleConfig.CannedMessageConfig] = Field(default=None)
    audio: Optional[ModuleConfig.AudioConfig] = Field(default=None)
    remote_hardware: Optional[ModuleConfig.RemoteHardwareConfig] = Field(default=None)
    neighbor_info: Optional[ModuleConfig.NeighborInfoConfig] = Field(default=None)
    ambient_lighting: Optional[ModuleConfig.AmbientLightingConfig] = Field(default=None)
    detection_sensor: Optional[ModuleConfig.DetectionSensorConfig] = Field(default=None)
    paxcounter: Optional[ModuleConfig.PaxcounterConfig] = Field(default=None)
    version: Optional[int] = Field(default=None)
