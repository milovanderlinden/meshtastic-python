from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class DeviceMetrics(BaseModel):
    """
    proto source: telemetry.proto
    message: DeviceMetrics
    """
    battery_level: Optional[int] = Field(default=None)
    voltage: Optional[float] = Field(default=None)
    channel_utilization: Optional[float] = Field(default=None, alias="channelUtilization")
    air_util_tx: Optional[float] = Field(default=None, alias="airUtilTx")
    uptime_seconds: Optional[int] = Field(default=None, alias="uptimeSeconds")


class EnvironmentMetrics(BaseModel):
    """
    proto source: telemetry.proto
    message: EnvironmentMetrics
    """
    temperature: Optional[float] = Field(default=None)
    relative_humidity: Optional[float] = Field(default=None)
    barometric_pressure: Optional[float] = Field(default=None)
    gas_resistance: Optional[float] = Field(default=None)
    voltage: Optional[float] = Field(default=None)
    current: Optional[float] = Field(default=None)
    iaq: Optional[int] = Field(default=None)
    distance: Optional[float] = Field(default=None)
    lux: Optional[float] = Field(default=None)
    white_lux: Optional[float] = Field(default=None)


class PowerMetrics(BaseModel):
    """
    proto source: telemetry.proto
    message: PowerMetrics
    """
    ch1_voltage: Optional[float] = Field(default=None)
    ch1_current: Optional[float] = Field(default=None)
    ch2_voltage: Optional[float] = Field(default=None)
    ch2_current: Optional[float] = Field(default=None)
    ch3_voltage: Optional[float] = Field(default=None)
    ch3_current: Optional[float] = Field(default=None)


class AirQualityMetrics(BaseModel):
    """
    proto source: telemetry.proto
    message: AirQualityMetrics
    """
    pm10_standard: Optional[int] = Field(default=None)
    pm25_standard: Optional[int] = Field(default=None)
    pm109_standard: Optional[int] = Field(default=None)
    pm10_environmental: Optional[int] = Field(default=None)
    pm25_environmental: Optional[int] = Field(default=None)
    pm100_environmental: Optional[int] = Field(default=None)
    particles_03um: Optional[int] = Field(default=None)
    particles_05um: Optional[int] = Field(default=None)
    particles_10um: Optional[int] = Field(default=None)
    particles_25um: Optional[int] = Field(default=None)
    particles_50um: Optional[int] = Field(default=None)
    particles_100um: Optional[int] = Field(default=None)


class Telemetry(BaseModel):
    """
    proto source: telemetry.proto
    message: Telemetry
    """
    time: Optional[int] = Field(default=None)

    # oneof variant
    device_metrics: Optional[DeviceMetrics] = Field(default=None)
    environment_metrics: Optional[EnvironmentMetrics] = Field(default=None)
    air_quality_metrics: Optional[AirQualityMetrics] = Field(default=None)
    power_metrics: Optional[PowerMetrics] = Field(default=None)
