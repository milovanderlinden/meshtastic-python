import math
import sys
from enum import Enum
from typing import List

import flet as ft

try:
    from meshtastic.schemas.mesh import NodeInfo
except ModuleNotFoundError:
    # see if we are in a development environment that does not have a compiled package
    from pathlib import Path
    path = str(Path(Path(__file__).parent.absolute()).parent.absolute().parent.absolute())
    sys.path.insert(0, path)
    from meshtastic.schemas.mesh import NodeInfo


class LatLon(str, Enum):
    LATITUDE = 'lat'
    LONGITUDE = 'lon'


def deg_to_dms(deg, direction: LatLon = LatLon.LATITUDE):
    decimals, number = math.modf(deg)
    d = int(number)
    m = int(decimals * 60)
    s = (deg - d - m / 60) * 3600.00
    compass = {
        'lat': ('N', 'S'),
        'lon': ('E', 'W')
    }
    compass_str = compass[direction.value][0 if d >= 0 else 1]
    return '{}º{}\'{:.0f}"{}'.format(abs(d), abs(m), abs(s), compass_str)


def get_avatar_color(value: str):
    colors_lookup = [
        ft.colors.AMBER,
        ft.colors.BLUE,
        ft.colors.BROWN,
        ft.colors.CYAN,
        ft.colors.GREEN,
        ft.colors.INDIGO,
        ft.colors.LIME,
        ft.colors.ORANGE,
        ft.colors.PINK,
        ft.colors.PURPLE,
        ft.colors.RED,
        ft.colors.TEAL,
        ft.colors.YELLOW,
    ]
    return colors_lookup[hash(value) % len(colors_lookup)]


def get_coordinates(node: NodeInfo, font_size: float) -> List[ft.Control]:
    """ Format the coordinates and return empty when none given"""
    _lon = 0
    _lat = 0
    if node.position:
        if node.position.latitude:
            _lat = node.position.latitude
        if node.position.longitude:
            _lat = node.position.longitude
    return [
        ft.Text(value=deg_to_dms(_lon, LatLon.LONGITUDE), size=font_size),
        ft.Text(value=deg_to_dms(_lat), size=font_size)
    ]


def get_short_name(node: NodeInfo) -> str:
    if node.user and node.user.short_name:
        return node.user.short_name
    return "None"


def get_long_name(node: NodeInfo) -> str:
    if node.user and node.user.long_name:
        return node.user.long_name
    return "Name not given"


class NodeComponent(ft.Container):
    def __init__(self, node_id: int):
        super().__init__()
        self.content = NodeRow(node_id)
        self.padding = 5
        self.width = 300
        self.alignment = ft.alignment.center
        self.border_radius = 10
        self.border = ft.border.all(0.5, ft.colors.WHITE)


class NodeRow(ft.Row):
    row_height = 18
    col_width = 100
    font_size = 10

    def __init__(self, node_id: int):
        super().__init__()
        # get the node info object
        node = NodeInfo(num=node_id)
        _short_name = get_short_name(node)
        _long_name = get_long_name(node)
        self.controls = [
            ft.CircleAvatar(
                radius=24,
                content=ft.Text(_short_name, size=self.font_size),
                bgcolor=get_avatar_color(_short_name),
            ),
            ft.Column(
                [
                    ft.Row(width=self.col_width-60, height=self.row_height, controls=[ft.Text(_long_name,
                                                                                              size=self.font_size)]),
                    ft.Row(width=self.col_width-60, height=self.row_height, controls=get_coordinates(node, self.font_size)),
                    # Coordinates or empty
                    ft.Row(width=self.col_width-60, height=self.row_height, controls=[
                        ft.Text(value="40m", selectable=True, size=self.font_size)
                    ]),
                ],
                tight=True,
                spacing=5,
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        width=self.col_width,
                        height=self.row_height,
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.Text("74%"),
                            ft.Icon(name=ft.icons.BATTERY_4_BAR,
                                    color=ft.colors.WHITE, size=18)
                        ]),
                    ft.Row(width=self.col_width, height=self.row_height, alignment=ft.MainAxisAlignment.END,
                           controls=[
                               ft.Text(value="2d", size=self.font_size),
                               ft.Icon(name=ft.icons.CALENDAR_TODAY, color=ft.colors.WHITE, size=18)
                           ]),
                    ft.Row(width=self.col_width, height=self.row_height, alignment=ft.MainAxisAlignment.END,
                           controls=[
                               ft.Text(value="ChUtil 1,1% AirUtilTX 0.6%", selectable=True, size=self.font_size)
                           ]),
                ],
                tight=True,
                spacing=5,
            ),
        ]

