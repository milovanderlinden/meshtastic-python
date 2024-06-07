import flet as ft
from flet_core import ControlEvent
from flet_navigator import PageData


class NavigationBar(ft.NavigationBar):

    def clicked(self, e: ControlEvent):
        if e == "default":
            nav_dest = 0
        else:
            nav_dest = e.control.selected_index
        if nav_dest == 1:
            self.pg.navigator.navigate('nodes', self.pg.page)
        elif nav_dest == 3:
            self.pg.navigator.navigate('devices', self.pg.page)

    def __init__(self, pg: PageData, selected_index: int = 0,):
        super().__init__()
        self.pg = pg
        self.selected_index = selected_index
        self.destinations = [
            ft.NavigationDestination(icon=ft.icons.CHAT),
            ft.NavigationDestination(icon=ft.icons.PEOPLE),
            ft.NavigationDestination(icon=ft.icons.MAP_OUTLINED),
            ft.NavigationDestination(icon=ft.icons.WIFI_TETHERING),
            ft.NavigationDestination(icon=ft.icons.SETTINGS_APPLICATIONS_OUTLINED),
        ]
        self.on_change = self.clicked
