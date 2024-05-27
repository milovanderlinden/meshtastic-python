from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field


class Type(IntEnum):
    """
    proto source: storeforward.proto
    enum: StoreAndForward.RequestResponse
    """
    UNSET = 0
    ROUTER_ERROR = 1
    ROUTER_HEARTBEAT = 2
    ROUTER_PING = 3
    ROUTER_PONG = 4
    ROUTER_BUSY = 5
    ROUTER_HISTORY = 6
    ROUTER_STATS = 7
    ROUTER_TEXT_DIRECT = 8
    ROUTER_TEXT_BROADCAST = 9
    CLIENT_ERROR = 64
    CLIENT_HISTORY = 65
    CLIENT_STATS = 66
    CLIENT_PING = 67
    CLIENT_PONG = 68
    CLIENT_ABORT = 106


class Statistics(BaseModel):
    """
    proto source: storeforward.proto
    enum: StoreAndForward.Statistics
    """
    messages_total: Optional[int] = Field(default=None)
    messages_saved: Optional[int] = Field(default=None)
    messages_max: Optional[int] = Field(default=None)
    up_time: Optional[int] = Field(default=None)
    requests: Optional[int] = Field(default=None)
    heartbeat: Optional[int] = Field(default=None)
    return_max: Optional[int] = Field(default=None)
    return_window: Optional[int] = Field(default=None)


class History(BaseModel):
    """
    proto source: storeforward.proto
    enum: StoreAndForward.History
    """
    history_messages: Optional[int] = Field(default=None)
    window: Optional[int] = Field(default=None)
    last_request: Optional[int] = Field(default=None)


class Heartbeat(BaseModel):
    """
    proto source: storeforward.proto
    enum: StoreAndForward.Heartbeat
    """
    period: Optional[int] = Field(default=None)
    secondary: Optional[int] = Field(default=None)


class StoreAndForward(BaseModel):
    """
    proto source: storeforward.proto
    message: StoreAndForward
    """
    rr: Optional[RequestResponse] = Field(default=None)
    # oneof variant
    stats: Optional[Statistics] = Field(default=None)
    history: Optional[History] = Field(default=None)
    heartbeat: Optional[Heartbeat] = Field(default=None)
    text: Optional[bytes] = Field(default=None)
