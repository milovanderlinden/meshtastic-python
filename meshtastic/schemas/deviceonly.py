from datetime import datetime
from enum import IntEnum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, model_validator
from .channel import Channel
from .localonly import LocalConfig, LocalModuleConfig
from .mesh import Position, User, DeviceMetrics, MyNodeInfo, MeshPacket, NodeRemoteHardwarePin


class PositionLite(BaseModel):
    """
    proto source: deviceonly.proto
    message: PositionLite
    """
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    altitude: Optional[int] = Field(default=None)
    time: Optional[datetime] = Field(default=None)
    location_source: Optional[Position.LocSource] = Field(default=None)

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
        return values

class NodeInfoLite(BaseModel):
    """
    proto source: deviceonly.proto
    message: NodeInfoLite
    """
    num: Optional[int] = Field(default=None)
    user: Optional[User] = Field(default=None)
    position: Optional[PositionLite] = Field(default=None)
    snr: Optional[float] = Field(default=None)
    last_heard: Optional[int] = Field(default=None)
    device_metrics: Optional[DeviceMetrics] = Field(default=None)
    channel: Optional[int] = Field(default=None)
    via_mqtt: Optional[bool] = Field(default=None)
    hops_away: Optional[int] = Field(default=None)
    is_favorite: Optional[bool] = Field(default=None)


class ScreenFonts(IntEnum):
    """
    proto source: deviceonly.proto
    enum: ScreenFonts
    """
    FONT_SMALL = 0
    FONT_MEDIUM = 1
    FONT_LARGE = 2


class DeviceState(BaseModel):
    """
    proto source: deviceonly.proto
    message: DeviceState
    """
    my_node: Optional[MyNodeInfo] = Field(default=None)
    owner: Optional[User] = Field(default=None)
    receive_queue: Optional[List[MeshPacket]] = Field(default=None)
    version: Optional[int] = Field(default=None)
    rx_text_message: Optional[MeshPacket] = Field(default=None)
    no_save: Optional[bool] = Field(default=None, deprecated=True)
    did_gps_reset: Optional[bool] = Field(default=None)
    rx_waypoint: Optional[MeshPacket] = Field(default=None)
    node_remote_hardware_pins: Optional[List[NodeRemoteHardwarePin]] = Field(default=None)
    node_db_lite: Optional[List[NodeInfoLite]] = Field(default=None)


class ChannelFile(BaseModel):
    """
    proto source: deviceonly.proto
    message: ChannelFile
    """
    channels: Optional[List[Channel]] = Field(default=None)
    version: Optional[int] = Field(default=None)


class OEMStore(BaseModel):
    """
    proto source: deviceonly.proto
    message: OEMStore
    """
    oem_icon_width: Optional[int] = Field(default=None)
    oem_icon_height: Optional[int] = Field(default=None)
    oem_icon_bits: Optional[bytes] = Field(default=None)
    oem_font: Optional[ScreenFonts] = Field(default=None)
    oem_text: Optional[str] = Field(default=None)
    oem_aes_key: Optional[bytes] = Field(default=None)
    oem_local_config: Optional[LocalConfig] = Field(default=None)
    oem_local_module_config: Optional[LocalModuleConfig] = Field(default=None)
