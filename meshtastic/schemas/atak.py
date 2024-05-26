from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field


class PLI(BaseModel):
    """
    proto source: atak.proto
    enum: Contact
    """
    latitude_i: Optional[int] = Field(default=None)
    longitude_i: Optional[int] = Field(default=None)
    altitude: Optional[int] = Field(default=None)
    speed: Optional[int] = Field(default=None)
    course: Optional[int] = Field(default=None)


class Contact(BaseModel):
    """
    proto source: atak.proto
    enum: Contact
    """
    callsign: Optional[str] = Field(default=None)
    device_callsign: Optional[str] = Field(default=None)


class Status(BaseModel):
    """
    proto source: atak.proto
    enum: Status
    """
    battery: Optional[int] = Field(default=None)


class MemberRole(IntEnum):
    """
    proto source: atak.proto
    enum: MemberRole
    """
    Unspecifed = 0  # Typo is in proto
    TeamMember = 1
    TeamLead = 2
    HQ = 3
    Sniper = 4
    Medic = 5
    ForwardObserver = 6
    RTO = 7
    K9 = 8


class Team(IntEnum):
    """
    proto source: atak.proto
    enum: Team
    """
    Unspecifed_Color = 0  # Typo is in proto
    White = 1
    Yellow = 2
    Orange = 3
    Magenta = 4
    Red = 5
    Maroon = 6
    Purple = 7
    Dark_Blue = 8
    Blue = 9
    Cyan = 10
    Teal = 11
    Green = 12
    Dark_Green = 13
    Brown = 14


class Group(BaseModel):
    """
    proto source: atak.proto
    message: Group
    """
    role: Optional[MemberRole] = Field(default=None)
    team: Optional[Team] = Field(default=None)


class GeoChat(BaseModel):
    """
    proto source: atak.proto
    message: GeoChat
    """
    message: Optional[str] = Field(default=None)
    to: Optional[str] = Field(default=None)


class TAKPacket(BaseModel):
    """
    proto source: atak.proto
    message: TAKPacket
    """
    is_compressed: Optional[bool] = Field(default=None)
    contact: Optional[Contact] = Field(default=None)
    group: Optional[Group] = Field(default=None)
    status: Optional[Status] = Field(default=None)
    PLI: Optional[PLI] = Field(default=None)
    chat: Optional[GeoChat] = Field(default=None)
