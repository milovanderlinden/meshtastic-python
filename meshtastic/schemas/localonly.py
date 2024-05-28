from typing import Optional

from pydantic import BaseModel, Field

from .config import DeviceConfig, PositionConfig, PowerConfig, NetworkConfig, DisplayConfig, LoRaConfig, BluetoothConfig
from .module_config import MQTTConfig, DetectionSensorConfig, SerialConfig, ExternalNotificationConfig, \
    StoreForwardConfig, RangeTestConfig, TelemetryConfig, CannedMessageConfig, AudioConfig, RemoteHardwareConfig, \
    NeighborInfoConfig, AmbientLightingConfig, PaxcounterConfig


class LocalConfig(BaseModel):
    """
    proto source: localonly.proto
    message: LocalConfig
    """
    device: Optional[DeviceConfig] = Field(default=None)
    position: Optional[PositionConfig] = Field(default=None)
    power: Optional[PowerConfig] = Field(default=None)
    network: Optional[NetworkConfig] = Field(default=None)
    display: Optional[DisplayConfig] = Field(default=None)
    lora: Optional[LoRaConfig] = Field(default=None)
    bluetooth: Optional[BluetoothConfig] = Field(default=None)
    version: Optional[int] = Field(default=None)


class LocalModuleConfig(BaseModel):
    """
    proto source: localonly.proto
    message: LocalModuleConfig
    """
    mqtt: Optional[MQTTConfig] = Field(default=None)
    serial: Optional[SerialConfig] = Field(default=None)
    external_notification: Optional[ExternalNotificationConfig] = Field(default=None)
    store_forward: Optional[StoreForwardConfig] = Field(default=None)
    range_test: Optional[RangeTestConfig] = Field(default=None)
    telemetry: Optional[TelemetryConfig] = Field(default=None)
    canned_message: Optional[CannedMessageConfig] = Field(default=None)
    audio: Optional[AudioConfig] = Field(default=None)
    remote_hardware: Optional[RemoteHardwareConfig] = Field(default=None)
    neighbor_info: Optional[NeighborInfoConfig] = Field(default=None)
    ambient_lighting: Optional[AmbientLightingConfig] = Field(default=None)
    detection_sensor: Optional[DetectionSensorConfig] = Field(default=None)
    paxcounter: Optional[PaxcounterConfig] = Field(default=None)
    version: Optional[int] = Field(default=None)
