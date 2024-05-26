from typing import Optional, List

from pydantic import BaseModel, Field

from .channel import ChannelSettings
from .config import Config


class ChannelSet(BaseModel):
    """
    module: apponly.proto
    message: ChannelSet
    """
    settings: Optional[List[ChannelSettings]] = Field(default=None)
    lora_config: Optional[Config.LoRaConfig] = Field(default=None)
