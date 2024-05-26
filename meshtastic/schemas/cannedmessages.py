from typing import Optional

from pydantic import BaseModel, Field


class CannedMessageModuleConfig(BaseModel):
    """
    module: cannedmessages.proto
    message: CannedMessageModuleConfig

    Predefined messages for canned message module separated by '|' characters.
    """
    messages: Optional[str] = Field(default=None)
