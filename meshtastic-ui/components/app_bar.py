import flet as ft
from .logo import small_black_logo


class AppBar(ft.AppBar):
    def __init__(self, title: str):
        super().__init__()
        self.leading_width = 40
        self.title = ft.Row([
            ft.Image(
                src=small_black_logo,
                height=30
            ),
            ft.Text(title)
        ])
        self.center_title = False
        self.color = "#000000"
        self.bgcolor = "#67ea94"
        self.actions = [
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
        ]

