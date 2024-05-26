from enum import IntEnum
from typing import Optional

from pydantic import BaseModel
from pydantic.v1 import Field


class XModem(BaseModel):
    """
    proto source: xmodel.proto
    message: XModem
    """
    class Control(IntEnum):
        """
        proto source: xmodel.proto
        message: XModem.Control
        """
        NUL = 0
        SOH = 1
        STX = 2
        EOT = 4
        ACK = 6
        NAK = 21
        CAN = 24
        CTRLZ = 26

    control: Optional[Control] = Field(default=None)
    seq: Optional[int] = Field(default=None)
    crc16: Optional[int] = Field(default=None)
    buffer: Optional[bytes] = Field(default=None)
