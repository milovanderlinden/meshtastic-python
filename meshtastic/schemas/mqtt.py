from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, model_validator
from .config import Role, RegionCode, ModemPreset
from .mesh import MeshPacket, HardwareModel


class ServiceEnvelope(BaseModel):
    """
    proto source: mqtt.proto
    message: ServiceEnvelope
    """
    packet: Optional[MeshPacket] = Field(default=None)
    channel_id: Optional[str] = Field(default=None)
    gateway_id: Optional[str] = Field(default=None)


class MapReport(BaseModel):
    """
    proto source: mqtt.proto
    message: ServiceEnvelope
    """
    long_name: Optional[str] = Field(default=None)
    short_name: Optional[str] = Field(default=None)
    role: Optional[Role] = Field(default=None)
    hw_model: Optional[HardwareModel] = Field(default=None)
    firmware_version: Optional[str] = Field(default=None)
    region: Optional[RegionCode] = Field(default=None)
    modem_preset: Optional[ModemPreset] = Field(default=None)
    has_default_channel: Optional[bool] = Field(default=None)
    latitude_i: Optional[int] = Field(default=None, alias="latitudeI")
    longitude_i: Optional[int] = Field(default=None, alias="longitudeI")
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    altitude: Optional[int] = Field(default=None)
    position_precision: Optional[int] = Field(default=None)
    num_online_local_nodes: Optional[int] = Field(default=None)

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
        return values
