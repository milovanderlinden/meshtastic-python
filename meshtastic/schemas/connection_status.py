from typing import Optional

from pydantic import BaseModel, Field


class SerialConnectionStatus(BaseModel):
    """
    module: connection_status.proto
    message: SerialConnectionStatus
    """
    baud: Optional[int] = Field(default=None)
    is_connected: Optional[bool] = Field(default=None)


class BluetoothConnectionStatus(BaseModel):
    """
    module: connection_status.proto
    message: BluetoothConnectionStatus
    """
    pin: Optional[int] = Field(default=None)
    rssi: Optional[int] = Field(default=None)
    is_connected: Optional[bool] = Field(default=None)


class NetworkConnectionStatus(BaseModel):
    """
    module: connection_status.proto
    message: NetworkConnectionStatus
    """
    ip_address: Optional[int] = Field(default=None)
    is_connected: Optional[bool] = Field(default=None)
    is_mqtt_connected: Optional[bool] = Field(default=None)
    is_syslog_connected: Optional[bool] = Field(default=None)


class EthernetConnectionStatus(BaseModel):
    """
    module: connection_status.proto
    message: EthernetConnectionStatus
    """
    status: Optional[NetworkConnectionStatus] = Field(default=None)


class WifiConnectionStatus(BaseModel):
    """
    module: connection_status.proto
    message: WifiConnectionStatus
    """
    status: Optional[NetworkConnectionStatus] = Field(default=None)
    ssid: Optional[str] = Field(default=None)
    rssi: Optional[int] = Field(default=None)


class DeviceConnectionStatus(BaseModel):
    """
    module: connection_status.proto
    message: DeviceConnectionStatus
    """
    # payload
    wifi: Optional[WifiConnectionStatus] = Field(default=None)
    ethernet: Optional[EthernetConnectionStatus] = Field(default=None)
    bluetooth: Optional[BluetoothConnectionStatus] = Field(default=None)
    serial: Optional[SerialConnectionStatus] = Field(default=None)
