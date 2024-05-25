from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, ValidationError


class ConfigDevice(BaseModel):
    role: Optional[str] = Field(default=None)
    serial_enabled: Optional[bool] = Field(default=None, alias="serialEnabled")
    node_info_broadcast_seconds: Optional[int] = Field(default=None, alias="nodeInfoBroadcastSecs")


class ConfigPosition(BaseModel):
    position_broadcast_seconds: Optional[int] = Field(default=None, alias="positionBroadcastSecs")
    position_broadcast_smart_enabled: Optional[bool] = Field(default=None, alias="positionBroadcastSmartEnabled")
    gps_update_interval: Optional[int] = Field(default=None, alias="gpsUpdateInterval")
    position_flags: Optional[int] = Field(default=None, alias="positionFlags")
    broadcast_smart_minimum_distance: Optional[int] = Field(default=None, alias="broadcastSmartMinimumDistance")
    broadcast_smart_minimum_interval_seconds: Optional[int] = Field(
        default=None,
        alias="broadcastSmartMinimumIntervalSecs"
    )
    gps_mode: Optional[str] = Field(default=None, alias="gpsMode")


class ConfigPower(BaseModel):
    wait_bluetooth_seconds: Optional[int] = Field(default=None, alias="waitBluetoothSecs")
    sds_seconds: Optional[int] = Field(default=None, alias="sdsSecs")
    ls_seconds: Optional[int] = Field(default=None, alias="lsSecs")
    minimum_wake_seconds: Optional[int] = Field(default=None, alias="minWakeSecs")


class ConfigNetwork(BaseModel):
    ntp_server: Optional[str] = Field(default=None, alias="ntpServer")


class ConfigDisplay(BaseModel):
    screen_on_seconds: Optional[int] = Field(default=None, alias="screenOnSecs")


class ConfigLora(BaseModel):
    use_preset: Optional[bool] = Field(default=None, alias="usePreset")
    region: Optional[str] = Field(default=None)
    hop_limit: Optional[int] = Field(default=None, alias="hopLimit")
    tx_enabled: Optional[bool] = Field(default=None, alias="txEnabled")
    tx_power: Optional[int] = Field(default=None, alias="txPower")
    sx_126x_rx_boosted_gain: Optional[bool] = Field(default=None, alias="sx126xRxBoostedGain")


class ConfigBluetooth(BaseModel):
    enabled: Optional[bool] = Field(default=None)
    mode: Optional[str] = Field(default=None)
    fixed_pin: Optional[int] = Field(default=None, alias="fixedPin")


class Config(BaseModel):
    device: Optional[ConfigDevice] = Field(default=None)
    position: Optional[ConfigPosition] = Field(default=None)
    power: Optional[ConfigPower] = Field(default=None)
    network: Optional[ConfigNetwork] = Field(default=None)
    display: Optional[ConfigDisplay] = Field(default=None)
    lora: Optional[ConfigLora] = Field(default=None)
    bluetooth: Optional[ConfigBluetooth] = Field(default=None)

    model_config = ConfigDict(validate_assignment=True)

    def update(self, **new_data):
        for field, value in new_data.items():
            # get the field for the given alias
            try:
                setattr(self, field, value)
            except ValidationError:
                for _f, meta in self.model_fields.items():
                    if meta.alias == field:
                        setattr(self, _f, value)
