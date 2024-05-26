from typing import Optional

from pydantic import BaseModel, Field

from .localonly import LocalConfig, LocalModuleConfig


class DeviceProfile(BaseModel):
    """
    module: clientonly.proto
    message: DeviceProfile
    """
    long_name: Optional[str] = Field(default=None)
    short_name: Optional[str] = Field(default=None)
    channel_url: Optional[str] = Field(default=None)
    config: Optional[LocalConfig] = Field(default=None)
    module_config: Optional[LocalModuleConfig] = Field(default=None)
