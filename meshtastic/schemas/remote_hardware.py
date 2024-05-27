from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field


class Type(IntEnum):
    """
    proto source: remote_hardware.proto
    enum: HardwareMessage.Type
    """
    UNSET = 0
    WRITE_GPIOS = 1
    WATCH_GPIOS = 2
    GPIOS_CHANGED = 3
    READ_GPIOS = 4
    READ_GPIOS_REPLY = 5


class HardwareMessage(BaseModel):
    """
    proto source: remote_hardware.proto
    message: HardwareMessage
    """
    type: Optional[Type] = Field(default=None)
    gpio_mask: Optional[int] = Field(default=None)
    gpio_value: Optional[int] = Field(default=None)
