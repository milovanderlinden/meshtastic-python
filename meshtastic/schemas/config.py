from enum import IntEnum, Enum
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, ValidationError


class Config(BaseModel):
    """
    module: config.proto
    message: Config
    """

    class DeviceConfig(BaseModel):
        """
        module: config.proto
        message: Config.DeviceConfig
        """

        class Role(IntEnum):
            """
            module: config.proto
            enum: Config.DeviceConfig.Role
            """
            CLIENT = 0
            CLIENT_MUTE = 1
            ROUTER = 2
            ROUTER_CLIENT = 3
            REPEATER = 4
            TRACKER = 5
            SENSOR = 6
            TAK = 7
            CLIENT_HIDDEN = 8
            LOST_AND_FOUND = 9
            TAK_TRACKER = 10

        class RebroadcastMode(IntEnum):
            """
            module: config.proto
            enum: Config.DeviceConfig.RebroadcastMode
            """
            ALL = 0
            ALL_SKIP_DECODING = 1
            LOCAL_ONLY = 2
            KNOWN_ONLY = 3

        role: Optional[Role] = Field(default=None)
        serial_enabled: Optional[bool] = Field(default=None, alias="serialEnabled")
        debug_log_enabled: Optional[bool] = Field(default=None)
        button_gpio: Optional[int] = Field(default=None)
        buzzer_gpio: Optional[int] = Field(default=None)
        rebroadcast_mode: Optional[RebroadcastMode] = Field(default=None)
        node_info_broadcast_secs: Optional[int] = Field(default=None, alias="nodeInfoBroadcastSecs")
        double_tap_as_button_press: Optional[bool] = Field(default=None)
        is_managed: Optional[bool] = Field(default=None)
        disable_triple_click: Optional[bool] = Field(default=None)
        tzdef: Optional[int] = Field(default=None)
        led_heartbeat_disabled: Optional[bool] = Field(default=None)

    class PositionConfig(BaseModel):
        """
        module: config.proto
        message: Config.PositionConfig
        """

        class PositionFlags(Enum):
            """
            module: config.proto
            enum: Config.PositionConfig.PositionFlag
            """
            UNSET = 0x0000
            ALTITUDE = 0x0001
            ALTITUDE_MSL = 0x0002
            GEOIDAL_SEPARATION = 0x0004
            DOP = 0x0008
            HVDOP = 0x0010
            SATINVIEW = 0x0020
            SEQ_NO = 0x0040
            TIMESTAMP = 0x0080
            HEADING = 0x0100
            SPEED = 0x0200

        class GpsMode(IntEnum):
            """
            module: config.proto
            enum: Config.PositionConfig.GpsMode
            """
            DISABLED = 0
            ENABLED = 1
            NOT_PRESENT = 2

        position_broadcast_secs: Optional[int] = Field(default=None, alias="positionBroadcastSecs")
        position_broadcast_smart_enabled: Optional[bool] = Field(default=None, alias="positionBroadcastSmartEnabled")
        fixed_position: Optional[bool] = Field(default=None)
        gps_enabled: Optional[bool] = Field(default=None, deprecated=True)
        gps_update_interval: Optional[int] = Field(default=None, alias="gpsUpdateInterval")
        gps_attempt_time: Optional[int] = Field(default=None, deprecated=True)
        # TODO why is the PositionFlags Enum not used?
        position_flags: Optional[int] = Field(default=None, alias="positionFlags")
        rx_gpio: Optional[int] = Field(default=None)
        tx_gpio: Optional[int] = Field(default=None)
        broadcast_smart_minimum_distance: Optional[int] = Field(default=None, alias="broadcastSmartMinimumDistance")
        broadcast_smart_minimum_interval_secs: Optional[int] = Field(
            default=None,
            alias="broadcastSmartMinimumIntervalSecs"
        )
        gps_en_gpio: Optional[int] = Field(default=None)
        gps_mode: Optional[GpsMode] = Field(default=None, alias="gpsMode")

    class PowerConfig(BaseModel):
        """
        module: config.proto
        message: Config.PowerConfig
        """
        is_power_saving: Optional[bool] = Field(default=None)
        on_battery_shutdown_after_secs: Optional[int] = Field(default=None)
        adc_multiplier_override: Optional[float] = Field(default=None)
        wait_bluetooth_secs: Optional[int] = Field(default=None, alias="waitBluetoothSecs")
        sds_secs: Optional[int] = Field(default=None, alias="sdsSecs")
        ls_secs: Optional[int] = Field(default=None, alias="lsSecs")
        min_wake_secs: Optional[int] = Field(default=None, alias="minWakeSecs")
        device_battery_ina_address: Optional[int] = Field(default=None)

    class NetworkConfig(BaseModel):
        """
        module: config.proto
        message: Config.NetworkConfig
        """
        class AddressMode(IntEnum):
            """
            module: config.proto
            enum: Config.NetworkConfig.AdressMode
            """
            DHCP = 0
            STATIC = 1

        class IpV4Config(BaseModel):
            """
            module: config.proto
            message: Config.NetworkConfig.IpV4Config
            """
            ip: Optional[int] = Field(default=None)
            gateway: Optional[int] = Field(default=None)
            subnet: Optional[int] = Field(default=None)
            dns: Optional[int] = Field(default=None)

        wifi_enabled: Optional[bool] = Field(default=None)
        wifi_ssid: Optional[str] = Field(default=None)
        wifi_psk: Optional[str] = Field(default=None)
        ntp_server: Optional[str] = Field(default=None, alias="ntpServer")
        eth_enabled: Optional[int] = Field(default=None)
        address_mode: Optional[AddressMode] = Field(default=None)
        ipv4_config: Optional[IpV4Config] = Field(default=None)
        rsyslog_server: Optional[str] = Field(default=None)

    class DisplayConfig(BaseModel):
        """
        module: config.proto
        message: Config.DisplayConfig
        """
        class GpsCoordinateFormat(IntEnum):
            """
            module: config.proto
            enum: Config.DisplayConfig.GpsCoordinateFormat
            """
            DEC = 0
            DMS = 1
            UTM = 2
            MGRS = 3
            OLC = 4
            OSGR = 5

        class DisplayUnits(IntEnum):
            """
            module: config.proto
            enum: Config.DisplayConfig.DisplayUnits
            """
            METRIC = 0
            IMPERIAL = 1

        class OledType(IntEnum):
            """
            module: config.proto
            enum: Config.DisplayConfig.OledType
            """
            OLED_AUTO = 0
            OLED_SSD1306 = 1
            OLED_SH1106 = 2
            OLED_SH1107 = 3

        class DisplayMode(IntEnum):
            """
            module: config.proto
            enum: Config.DisplayConfig.DisplayMode
            """
            DEFAULT = 0
            TWOCOLOR = 1
            INVERTED = 2
            COLOR = 3

        screen_on_secs: Optional[int] = Field(default=None, alias="screenOnSecs")
        gps_format: Optional[GpsCoordinateFormat] = Field(default=None)
        auto_screen_carousel_secs: Optional[int] = Field(default=None)
        compass_north_top: Optional[bool] = Field(default=None)
        flip_screen: Optional[bool] = Field(default=None)
        units: Optional[DisplayUnits] = Field(default=None)
        oled: Optional[OledType] = Field(default=None)
        displaymode: Optional[DisplayMode] = Field(default=None)
        heading_bold: Optional[bool] = Field(default=None)
        wake_on_tap_or_motion: Optional[bool] = Field(default=None)

    class LoRaConfig(BaseModel):
        """
        module: config.proto
        message: Config.LoRaConfig
        """
        class RegionCode(IntEnum):
            """
            module: config.proto
            enum: Config.LoRaConfig.RegionCode
            """
            UNSET = 0
            US = 1
            EU_433 = 2
            EU_868 = 3
            CN = 4
            JP = 5
            ANZ = 6
            KR = 7
            TW = 8
            RU = 9
            IN = 10
            NZ_865 = 11
            TH = 12
            LORA_24 = 13
            UA_433 = 14
            UA_868 = 15
            MY_433 = 16
            MY_919 = 17
            SG_923 = 18

        class ModemPreset(IntEnum):
            """
            module: config.proto
            enum: Config.LoRaConfig.ModemPreset
            """
            LONG_FAST = 0
            LONG_SLOW = 1
            VERY_LONG_SLOW = 2
            MEDIUM_SLOW = 3
            MEDIUM_FAST = 4
            SHORT_SLOW = 5
            SHORT_FAST = 6
            LONG_MODERATE = 7

        use_preset: Optional[bool] = Field(default=None, alias="usePreset")
        modem_preset: Optional[ModemPreset] = Field(default=None)
        bandwidth: Optional[int] = Field(default=None)
        spread_factor: Optional[int] = Field(default=None)
        coding_rate: Optional[int] = Field(default=None)
        frequency_offset: Optional[float] = Field(default=None)
        region: Optional[RegionCode] = Field(default=None)
        hop_limit: Optional[int] = Field(default=None, alias="hopLimit")
        tx_enabled: Optional[bool] = Field(default=None, alias="txEnabled")
        tx_power: Optional[int] = Field(default=None, alias="txPower")
        channel_num: Optional[int] = Field(default=None)
        override_duty_cycle: Optional[bool] = Field(default=None)
        sx_126x_rx_boosted_gain: Optional[bool] = Field(default=None, alias="sx126xRxBoostedGain")
        override_frequency: Optional[float] = Field(default=None)
        ignore_incoming: Optional[List[int]] = Field(default=None)
        ignore_mqtt: Optional[bool] = Field(default=None)

    class BluetoothConfig(BaseModel):
        """
        module: config.proto
        message: Config.BluetoothConfig
        """
        class PairingMode(IntEnum):
            """
            module: config.proto
            enum: Config.BluetoothConfig.PairingMode
            """
            RANDOM_PIN = 0
            FIXED_PIN = 1
            NO_PIN = 2

        enabled: Optional[bool] = Field(default=None)
        mode: Optional[PairingMode] = Field(default=None)
        fixed_pin: Optional[int] = Field(default=None, alias="fixedPin")

    # Payload
    device: Optional[DeviceConfig] = Field(default=None)
    position: Optional[PositionConfig] = Field(default=None)
    power: Optional[PowerConfig] = Field(default=None)
    network: Optional[NetworkConfig] = Field(default=None)
    display: Optional[DisplayConfig] = Field(default=None)
    lora: Optional[LoRaConfig] = Field(default=None)
    bluetooth: Optional[BluetoothConfig] = Field(default=None)

    # Model magic
    model_config = ConfigDict(validate_assignment=True)

    def update(self, **new_data):
        for field, value in new_data.items():
            # get the field for the given alias
            try:
                setattr(self, field, value)
            except ValidationError:
                for _f, meta in self.model_fields.items():
                    if meta.alias == field:
                        setattr(self, _f, value)
