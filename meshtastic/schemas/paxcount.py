from typing import Optional

from pydantic import BaseModel, Field


class Paxcount(BaseModel):
    """
    proto source: paxcount.proto
    message: Paxcount
    """
    wifi: Optional[int] = Field(default=None)
    ble: Optional[int] = Field(default=None)
    uptime: Optional[int] = Field(default=None)
