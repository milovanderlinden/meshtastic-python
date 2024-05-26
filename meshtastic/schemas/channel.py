from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ModuleSettings(BaseModel):
    """
    proto source: channel.proto
    message: ModuleSettings
    """
    position_precision: Optional[int] = Field(default=None, alias="positionPrecision")
    is_client_muted: Optional[bool] = Field(default=None)


class ChannelSettings(BaseModel):
    """
    proto source: channel.proto
    message: ChannelSettings
    """

    channel: Optional[int] = Field(default=None, deprecated=True)
    psk: Optional[bytes] = Field(default=None)
    name: Optional[str] = Field(default=None)
    id: Optional[int] = Field(default=None)
    uplink_enabled: Optional[bool] = Field(default=None)
    downlink_enabled: Optional[bool] = Field(default=None)
    module_settings: Optional[ModuleSettings] = Field(default=None, alias="moduleSettings")
    role: Optional[str] = Field(default=None)


class Channel(BaseModel):
    """
    proto source: channel.proto
    message: Channel
    """
    class Role(str, Enum):
        DISABLED = 'DISABLED'
        PRIMARY = 'PRIMARY'
        SECONDARY = 'SECONDARY'

    # payload
    index: Optional[int] = Field(default=0)
    settings: Optional[ChannelSettings] = Field(default={})
    role: Optional[Role] = Field(default=None)
