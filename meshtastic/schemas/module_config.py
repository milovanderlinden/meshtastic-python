from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ModuleConfigMqttMapReportingSettings(BaseModel):
    position_precision: Optional[int] = Field(default=None, alias="positionPrecision")


class ModuleConfigMqtt(BaseModel):
    address: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    encryption_enabled: Optional[bool] = Field(default=None, alias="encryptionEnabled")
    proxy_to_client_enabled: Optional[bool] = Field(default=None, alias="proxyToClientEnabled")
    map_reporting_enabled: Optional[bool] = Field(default=None, alias="mapReportingEnabled")
    map_reporting_settings: Optional[ModuleConfigMqttMapReportingSettings] = Field(
        default=None,
        alias="mapReportingSettings"
    )


class ModuleConfigSerial(BaseModel):
    """ Needs defining """


class ModuleConfigExternalNotification(BaseModel):
    """ Needs defining """


class ModuleConfigStoreForward(BaseModel):
    """ Needs defining """


class ModuleConfigRangeTest(BaseModel):
    """ Needs defining """


class ModuleConfigTelemetry(BaseModel):
    device_update_interval: Optional[int] = Field(default=None, alias="deviceUpdateInterval")
    environment_update_interval: Optional[int] = Field(default=None, alias="environmentUpdateInterval")
    air_quality_interval: Optional[int] = Field(default=None, alias="airQualityInterval")
    power_measurement_enabled: Optional[bool] = Field(default=None, alias="powerMeasurementEnabled")
    power_screen_enabled: Optional[bool] = Field(default=None, alias="powerScreenEnabled")


class ModuleConfigCannedMessage(BaseModel):
    """ Needs defining """


class ModuleConfigAudio(BaseModel):
    """ Needs defining """


class ModuleConfigRemoteHardware(BaseModel):
    """ Needs defining """


class ModuleConfigNeighborInfo(BaseModel):
    """ Needs defining """


class ModuleConfigAmbientLighting(BaseModel):
    current: Optional[int] = Field(default=None)
    red: Optional[int] = Field(default=None)
    green: Optional[int] = Field(default=None)
    blue: Optional[int] = Field(default=None)


class ModuleConfigDetectionSensor(BaseModel):
    minimum_broadcast_seconds: Optional[int] = Field(default=None, alias="minimumBroadcastSecs")
    detection_triggered_high: Optional[bool] = Field(default=None, alias="detectionTriggeredHigh")


class ModuleConfigPaxCounter(BaseModel):
    """ Needs defining """


class ModuleConfig(BaseModel):
    mqtt: Optional[ModuleConfigMqtt] = Field(default=None)
    serial: Optional[ModuleConfigSerial] = Field(default=None)
    external_notification: Optional[ModuleConfigExternalNotification] = Field(
        default=None,
        alias="externalNotification"
    )
    store_forward: Optional[ModuleConfigStoreForward] = Field(default=None, alias="storeForward")
    range_test: Optional[ModuleConfigRangeTest] = Field(default=None, alias="rangeTest")
    telemetry: Optional[ModuleConfigTelemetry] = Field(default=None)
    canned_message: Optional[ModuleConfigCannedMessage] = Field(default=None, alias="cannedMessage")
    audio: Optional[ModuleConfigAudio] = Field(default=None)
    remote_hardware: Optional[ModuleConfigRemoteHardware] = Field(default=None, alias="remoteHardware")
    neighbor_info: Optional[ModuleConfigNeighborInfo] = Field(default=None, alias="neighborInfo")
    ambient_lighting: Optional[ModuleConfigAmbientLighting] = Field(default=None, alias="ambientLighting")
    detection_sensor: Optional[ModuleConfigDetectionSensor] = Field(default=None, alias="detectionSensor")
    pax_counter: Optional[ModuleConfigPaxCounter] = Field(default=None, alias="paxcounter")

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
