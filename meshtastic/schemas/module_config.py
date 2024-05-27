from enum import IntEnum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class RemoteHardwarePinType(IntEnum):
    """
    proto source: module_config.proto
    enum: emoteHardwarePin.RemoteHardwarePinType
    """
    UNKNOWN = 0
    DIGITAL_READ = 1
    DIGITAL_WRITE = 2


class RemoteHardwarePin(BaseModel):
    """
    proto source: module_config.proto
    message: RemoteHardwarePin
    """
    gpio_pin: Optional[int] = Field(default=None)
    name: Optional[int] = Field(default=None)
    type: Optional[RemoteHardwarePinType] = Field(default=None)


class MapReportSettings(BaseModel):
    """
    proto source: module_config.proto
    message: ModuleConfig.MQTTConfig.MapReportSettings
    """
    publish_interval_secs: Optional[int] = Field(default=None)
    position_precision: Optional[int] = Field(default=None, alias="positionPrecision")


class MQTTConfig(BaseModel):
    """
    proto source: module_config.proto
    message: ModuleConfig.MQTTConfig
    """
    enabled: Optional[bool] = Field(default=None)
    address: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    encryption_enabled: Optional[bool] = Field(default=None, alias="encryptionEnabled")
    json_enabled: Optional[bool] = Field(default=None)
    tls_enabled: Optional[bool] = Field(default=None)
    root: Optional[bool] = Field(default=None)
    proxy_to_client_enabled: Optional[bool] = Field(default=None, alias="proxyToClientEnabled")
    map_reporting_enabled: Optional[bool] = Field(default=None, alias="mapReportingEnabled")
    map_report_settings: Optional[MapReportSettings] = Field(
        default=None,
        alias="mapReportingSettings"
    )


class RemoteHardwareConfig(BaseModel):
    """
    proto source: module_config.proto
    message: ModuleConfig.RemoteHardwareConfig
    """
    enabled: Optional[bool] = Field(default=None)
    allow_undefined_pin_access: Optional[bool] = Field(default=None)
    available_pins: Optional[List[RemoteHardwarePin]] = Field(default=None)


class NeighborInfoConfig(BaseModel):
    """
    proto source: module_config.proto
    message: NeighborInfoConfig
    """
    enabled: Optional[bool] = Field(default=None)
    update_interval: Optional[int] = Field(default=None)


class DetectionSensorConfig(BaseModel):
    """
    proto source: module_config.proto
    message: DetectionSensorConfig
    """
    enabled: Optional[bool] = Field(default=None)
    minimum_broadcast_secs: Optional[int] = Field(default=None, alias="minimumBroadcastSecs")
    state_broadcast_secs: Optional[int] = Field(default=None)
    send_bell: Optional[bool] = Field(default=None)
    name: Optional[bool] = Field(default=None)
    monitor_pin: Optional[int] = Field(default=None)
    detection_triggered_high: Optional[bool] = Field(default=None, alias="detectionTriggeredHigh")
    use_pullup: Optional[bool] = Field(default=None)


class Audio_Baud(IntEnum):
    CODEC2_DEFAULT = 0
    CODEC2_3200 = 1
    CODEC2_2400 = 2
    CODEC2_1600 = 3
    CODEC2_1400 = 4
    CODEC2_1300 = 5
    CODEC2_1200 = 6
    CODEC2_700 = 7
    CODEC2_700B = 8


class AudioConfig(BaseModel):
    """
    proto source: module_config.proto
    message: AudioConfig
    """
    codec2_enabled: Optional[bool] = Field(default=None)
    ptt_pin: Optional[int] = Field(default=None)
    bitrate: Optional[Audio_Baud] = Field(default=None)
    i2s_ws: Optional[int] = Field(default=None)
    i2s_sd: Optional[int] = Field(default=None)
    i2s_din: Optional[int] = Field(default=None)
    i2s_sck: Optional[int] = Field(default=None)


class PaxcounterConfig(BaseModel):
    """
    proto source: module_config.proto
    message: PaxcounterConfig
    """
    enabled: Optional[bool] = Field(default=None)
    paxcounter_update_interval: Optional[int] = Field(default=None)
    wifi_threshold: Optional[int] = Field(default=None)
    ble_threshold: Optional[int] = Field(default=None)


class Serial_Baud(IntEnum):
    BAUD_DEFAULT = 0
    BAUD_110 = 1
    BAUD_300 = 2
    BAUD_600 = 3
    BAUD_1200 = 4
    BAUD_2400 = 5
    BAUD_4800 = 6
    BAUD_9600 = 7
    BAUD_19200 = 8
    BAUD_38400 = 9
    BAUD_57600 = 10
    BAUD_115200 = 11
    BAUD_230400 = 12
    BAUD_460800 = 13
    BAUD_576000 = 14
    BAUD_921600 = 15


class Serial_Mode(IntEnum):
    DEFAULT = 0
    SIMPLE = 1
    PROTO = 2
    TEXTMSG = 3
    NMEA = 4
    # NMEA messages specifically tailored for CalTopo
    CALTOPO = 5


class SerialConfig(BaseModel):
    """
    proto source: module_config.proto
    message: SerialConfig
    """
    enabled: Optional[bool] = Field(default=None)
    echo: Optional[bool] = Field(default=None)
    rxd: Optional[int] = Field(default=None)
    txd: Optional[int] = Field(default=None)
    baud: Optional[Serial_Baud] = Field(default=None)
    timeout: Optional[int] = Field(default=None)
    mode: Optional[Serial_Mode] = Field(default=None)
    override_console_serial_port: Optional[bool] = Field(default=None)


class ExternalNotificationConfig(BaseModel):
    """
    proto source: module_config.proto
    message: ExternalNotificationConfig
    """
    enabled: Optional[bool] = Field(default=None)
    output_ms: Optional[int] = Field(default=None)
    output: Optional[int] = Field(default=None)
    output_vibra: Optional[int] = Field(default=None)
    output_buzzer: Optional[int] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    alert_message: Optional[bool] = Field(default=None)
    alert_message_vibra: Optional[bool] = Field(default=None)
    alert_message_buzzer: Optional[bool] = Field(default=None)
    alert_bell: Optional[bool] = Field(default=None)
    alert_bell_vibra: Optional[bool] = Field(default=None)
    alert_bell_buzzer: Optional[bool] = Field(default=None)
    use_pwm: Optional[bool] = Field(default=None)
    nag_timeout: Optional[int] = Field(default=None)
    use_i2s_as_buzzer: Optional[bool] = Field(default=None)


class StoreForwardConfig(BaseModel):
    """
    proto source: module_config.proto
    message: StoreForwardConfig
    """
    enabled: Optional[bool] = Field(default=None)
    heartbeat: Optional[bool] = Field(default=None)
    records: Optional[int] = Field(default=None)
    history_return_max: Optional[int] = Field(default=None)
    history_return_window: Optional[int] = Field(default=None)


class RangeTestConfig(BaseModel):
    """
    proto source: module_config.proto
    message: RangeTestConfig
    """
    enabled: Optional[bool] = Field(default=None)
    sender: Optional[int] = Field(default=None)
    save: Optional[bool] = Field(default=None)


class TelemetryConfig(BaseModel):
    """
    proto source: module_config.proto
    message: TelemetryConfig
    """
    device_update_interval: Optional[int] = Field(default=None, alias="deviceUpdateInterval")
    environment_update_interval: Optional[int] = Field(default=None, alias="environmentUpdateInterval")
    environment_measurement_enabled: Optional[bool] = Field(default=None)
    environment_screen_enabled: Optional[bool] = Field(default=None)
    environment_display_fahrenheit: Optional[bool] = Field(default=None)
    air_quality_enabled: Optional[bool] = Field(default=None)
    air_quality_interval: Optional[int] = Field(default=None, alias="airQualityInterval")
    power_measurement_enabled: Optional[bool] = Field(default=None, alias="powerMeasurementEnabled")
    power_update_interval: Optional[bool] = Field(default=None)
    power_screen_enabled: Optional[bool] = Field(default=None, alias="powerScreenEnabled")


class InputEventChar(IntEnum):
    NONE = 0
    UP = 17
    DOWN = 18
    LEFT = 19
    RIGHT = 20
    SELECT = 10
    BACK = 27
    CANCEL = 24


class CannedMessageConfig(BaseModel):
    """
    proto source: module_config.proto
    message: CannedMessageConfig
    """
    rotary1_enabled: Optional[bool] = Field(default=None)
    inputbroker_pin_a: Optional[int] = Field(default=None)
    inputbroker_pin_b: Optional[int] = Field(default=None)
    inputbroker_pin_press: Optional[int] = Field(default=None)
    inputbroker_event_cw: Optional[InputEventChar] = Field(default=None)
    inputbroker_event_ccw: Optional[InputEventChar] = Field(default=None)
    inputbroker_event_press: Optional[InputEventChar] = Field(default=None)
    updown1_enabled: Optional[bool] = Field(default=None)
    enabled: Optional[bool] = Field(default=None)
    allow_input_source: Optional[str] = Field(default=None)
    send_bell: Optional[bool] = Field(default=None)


class AmbientLightingConfig(BaseModel):
    """
    proto source: module_config.proto
    message: AmbientLightingConfig
    """
    led_state: Optional[bool] = Field(default=None)
    current: Optional[int] = Field(default=None)
    red: Optional[int] = Field(default=None)
    green: Optional[int] = Field(default=None)
    blue: Optional[int] = Field(default=None)


class ModuleConfig(BaseModel):
    """
    proto source: module_config.proto
    message: ModuleConfig
    """

    mqtt: Optional[MQTTConfig] = Field(default=None)
    serial: Optional[SerialConfig] = Field(default=None)
    external_notification: Optional[ExternalNotificationConfig] = Field(
        default=None,
        alias="externalNotification"
    )
    store_forward: Optional[StoreForwardConfig] = Field(default=None, alias="storeForward")
    range_test: Optional[RangeTestConfig] = Field(default=None, alias="rangeTest")
    telemetry: Optional[TelemetryConfig] = Field(default=None)
    canned_message: Optional[CannedMessageConfig] = Field(default=None, alias="cannedMessage")
    audio: Optional[AudioConfig] = Field(default=None)
    remote_hardware: Optional[RemoteHardwareConfig] = Field(default=None, alias="remoteHardware")
    neighbor_info: Optional[NeighborInfoConfig] = Field(default=None, alias="neighborInfo")
    ambient_lighting: Optional[AmbientLightingConfig] = Field(default=None, alias="ambientLighting")
    detection_sensor: Optional[DetectionSensorConfig] = Field(default=None, alias="detectionSensor")
    paxcounter: Optional[PaxcounterConfig] = Field(default=None, alias="paxcounter")

    model_config = ConfigDict(validate_assignment=True, populate_by_name=True)

    def update(self, **new_data):
        for field, value in new_data.items():
            # get the field for the given alias
            try:
                setattr(self, field, value)
            except ValidationError:
                for _f, meta in self.model_fields.items():
                    if meta.alias == field:
                        setattr(self, _f, value)
