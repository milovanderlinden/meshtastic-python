from typing import Optional

from pydantic import BaseModel, Field


class ChannelModuleSettings(BaseModel):
    position_precision: Optional[int] = Field(default=None, alias="positionPrecision")


class ChannelSettings(BaseModel):
    psk: Optional[str] = Field(default=None)
    module_settings: Optional[ChannelModuleSettings] = Field(default=None, alias="moduleSettings")
    role: Optional[str] = Field(default=None)


class Channel(BaseModel):
    index: Optional[int] = Field(default=0)
    settings: Optional[ChannelSettings] = Field(default={})
