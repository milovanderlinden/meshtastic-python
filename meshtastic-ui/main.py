import flet as ft
from components import AppBar, NavigationBar, NodeGridComponent


def main(page: ft.Page) -> None:
    page.title = "Meshtastic - python"

    def route_change(e: ft.RouteChangeEvent) -> None:
        page.views.clear()

        page.views.append(
            ft.View(
                route="/",
                controls=[
                    AppBar("Home"),
                    ft.Text(value="Home", size=30),
                    ft.ElevatedButton(text='Show nodes', on_click=lambda _: page.go('/nodes')),
                    ft.ElevatedButton(text='Show devices', on_click=lambda _: page.go('/devices')),
                    NavigationBar(0)
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=26
            )
        )

        if page.route == '/nodes':
            page.views.append(
                ft.View(
                    route="/nodes",
                    controls=[
                        AppBar("Nodes"),
                        ft.Text(value="Nodes", size=30),
                        ft.ElevatedButton(text='Back', on_click=lambda _: page.go('/')),
                        NavigationBar(4),
                        NodeGridComponent()
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        if page.route == '/devices':
            cg = ft.RadioGroup(content=ft.Column([
                ft.Radio(value="red", label="None"),
                ft.Radio(value="green", label="Meshtastic_9e14")]), value="red")

            page.views.append(
                ft.View(
                    route="/devices",
                    controls=[
                        AppBar("Devices"),
                        ft.Text(value="Devices", size=30),
                        ft.ElevatedButton(text='Back', on_click=lambda _: page.go('/')),
                        NavigationBar(3),
                        ft.Text("Not connected, select radio below"),
                        cg
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        page.update()

    def view_pop(e: ft.ViewPopEvent) -> None:
        page.views.pop()
        top_view: ft.View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main)


