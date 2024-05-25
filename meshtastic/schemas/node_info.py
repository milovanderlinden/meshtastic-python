""" es component """
import base64
import re
from datetime import datetime
from typing import Optional, Dict, Any, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class Power(BaseModel):
    """ Power Class """
    battery: Optional[int] = Field(default=None, alias="Battery")
    usb_power: Optional[int] = Field(default=None, alias="usbPower")
    is_charging: Optional[int] = Field(default=None, alias="isCharging")
    bat_mv: Optional[int] = Field(default=None, alias="batMv")
    bat_pct: Optional[int] = Field(default=None, alias="batPct")


class User(BaseModel):
    """ User Class """
    id: Optional[str] = Field(default=None)
    mac_address: Optional[str] = Field(default=None, alias="macaddr")
    hardware_model: Optional[str] = Field(default=None, alias="hwModel")
    role: Optional[str] = Field(default=None)
    short_name: Optional[str] = Field(default=None, alias="shortName")
    long_name: Optional[str] = Field(default=None, alias="longName")

    @field_validator('mac_address', mode='before')
    @classmethod
    def mac_validator(cls, v: str):
        """
        Convert the base 64 encoded value to a mac address
        val - base64 encoded value (ex: '/c0gFyhb')
        returns: a string formatted like a mac address (ex: 'fd:cd:20:17:28:5b')
        """
        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", v):
            val_as_bytes = base64.b64decode(v)
            return ":".join(f"{x:02x}" for x in val_as_bytes)
        return v


class DeviceMetrics(BaseModel):
    """ Device Metrics Class """
    channel_utilization: Optional[float] = Field(default=None, alias="channelUtilization")
    air_util_tx: Optional[float] = Field(default=None, alias="airUtilTx")
    uptime_seconds: Optional[int] = Field(default=None, alias="uptimeSeconds")


class Position(BaseModel):
    """ Position Class """
    time: Optional[Union[datetime]] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    altitude: Optional[int] = Field(default=None)
    latitude_i: Optional[int] = Field(default=None, alias="latitudeI", exclude=True)
    longitude_i: Optional[int] = Field(default=None, alias="longitudeI", exclude=True)

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
        print(values)
        return values


class NodeInfo(BaseModel):
    """ Class to bundle node information """
    num: Optional[int] = Field(default=None)
    user: Optional[User] = Field(default=None)
    position: Optional[Position] = Field(default=None)
    snr: Optional[float] = Field(default=None)
    last_heard: Optional[int] = Field(default=None, alias="lastHeard")
    device_metrics: Optional[DeviceMetrics] = Field(default=None, alias="deviceMetrics")
    is_favorite: Optional[bool] = Field(default=None, alias="isFavorite")


class Info(BaseModel):
    """ Node Info Class """
    node_number: Optional[int] = Field(default=None, alias="myNodeNum")
    reboot_count: Optional[int] = Field(default=None, alias="rebootCount")
    minimal_application_version: Optional[int] = Field(default=None, alias="minAppVersion")


class Metadata(BaseModel):
    firmwareVersion: Optional[str] = Field(default=None, alias="firmwareVersion")
    device_state_version: Optional[int] = Field(default=None, alias='deviceStateVersion')
    can_shutdown: Optional[bool] = Field(default=None, alias='canShutdown')
    has_wifi: Optional[bool] = Field(default=None, alias='hasWifi')
    has_bluetooth: Optional[bool] = Field(default=None, alias='hasBluetooth')
    role: Optional[str] = Field(default=None)
    position_flags: Optional[int] = Field(default=None, alias='positionFlags')
    hardware_model: Optional[str] = Field(default=None, alias='hwModel')
