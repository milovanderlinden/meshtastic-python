import flet as ft


class NavigationBar(ft.NavigationBar):
    def __init__(self, selected_index: int = 0):
        super().__init__()
        self.selected_index = selected_index
        self.destinations = [
            ft.NavigationDestination(icon=ft.icons.CHAT),
            ft.NavigationDestination(icon=ft.icons.PEOPLE),
            ft.NavigationDestination(icon=ft.icons.MAP_OUTLINED),
            ft.NavigationDestination(icon=ft.icons.WIFI_TETHERING),
            ft.NavigationDestination(icon=ft.icons.SETTINGS_APPLICATIONS_OUTLINED),
        ]
