import flet as ft
from components import small_black_logo, NodeComponent


def main(page: ft.Page):

    appbar = ft.AppBar(
        leading_width=40,
        title=ft.Image(
            src=small_black_logo,
            height=30,
        ),
        center_title=False,
        color="#000000",
        bgcolor="#67ea94",
        actions=[
            ft.IconButton(ft.icons.CLOUD_OFF),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Debug panel"),
                    ft.PopupMenuItem(text="Radio configuration"),
                    ft.PopupMenuItem(text="Export rangetest.csv"),
                    ft.PopupMenuItem(text="Theme"),
                    ft.PopupMenuItem(text="Language"),
                    ft.PopupMenuItem(text="Show introduction"),
                    ft.PopupMenuItem(text="Quick chat options"),
                    ft.PopupMenuItem(text="About"),

                ]
            ),
        ],
    )
    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="red", label="None"),
        ft.Radio(value="green", label="Meshtastic_9e14")]), value="red")
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.HIDDEN
    page.padding = ft.padding.Padding(20, 10, 0, 20)

    floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, bgcolor="#67ea94", foreground_color="#000000"
    )

    navigation_bar = ft.NavigationBar(
        selected_index=4,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CHAT),
            ft.NavigationDestination(icon=ft.icons.PEOPLE),
            ft.NavigationDestination(icon=ft.icons.MAP_OUTLINED),
            ft.NavigationDestination(icon=ft.icons.WIFI_TETHERING),
            ft.NavigationDestination(icon=ft.icons.SETTINGS_APPLICATIONS_OUTLINED),
        ]
    )
    page.add(
        appbar,
        ft.Text("Not connected, select radio below"),
        cg,
        floating_action_button,
        navigation_bar
    )
    for i in range (0, 12):
        page.add(NodeComponent(i))


ft.app(target=main)
