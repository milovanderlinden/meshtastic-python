from typing import Optional

from pydantic import BaseModel, Field


class RTTTLConfig(BaseModel):
    """
    proto source: rtttl.proto
    message: RTTTLConfig
    """

    ringtone: Optional[str] = Field(default=None)
