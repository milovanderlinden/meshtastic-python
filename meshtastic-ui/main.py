import flet as ft
from flet_navigator import VirtualFletNavigator, ROUTE_404, NavigatorAnimation
from flet_navigator import PageData, route
from components import AppBar, NavigationBar, NodeGridComponent


@route('/')
def main_page(pg: PageData) -> None:
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER,
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    pg.page.spacing = 26
    pg.page.add(
        AppBar("Home"),
        ft.Text(value="Home", size=30),
        ft.ElevatedButton(text='Show nodes', on_click=lambda _: pg.navigator.navigate('nodes', pg.page)),
        ft.ElevatedButton(text='Show devices', on_click=lambda _: pg.navigator.navigate('devices', pg.page)),
        NavigationBar(pg, 0)
    )


@route('nodes')
def nodes_page(pg: PageData) -> None:
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER,
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    pg.page.spacing = 26
    pg.page.add(
        AppBar("Nodes"),
        ft.Text(value="Nodes", size=30),
        ft.ElevatedButton(text='Back', on_click=lambda _: pg.navigator.navigate('/', pg.page)),
        NavigationBar(pg, 1),
        NodeGridComponent()
    )


@route('devices')
def devices_page(pg: PageData) -> None:
    pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER,
    pg.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    pg.page.spacing = 26
    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="red", label="None"),
        ft.Radio(value="green", label="Meshtastic_9e14")]), value="red")
    pg.page.add(
        AppBar("Devices"),
        ft.Text(value="Devices", size=30),
        ft.ElevatedButton(text='Back', on_click=lambda _: pg.navigator.navigate('/', pg.page)),
        NavigationBar(pg, 3),
        ft.Text("Not connected, select radio below"),
        cg
    )


def route_404(pg: PageData) -> None:
    pg.page.add(ft.Text(f'404'))


def main(page: ft.Page) -> None:
    # Initialize navigator.
    flet_navigator = VirtualFletNavigator(
        routes={
            '/': main_page,
            'nodes': nodes_page,
            'devices': devices_page,
            ROUTE_404: route_404  # 404 page route.
        },
        # route_changed_handler=lambda _route: print(f'Route changed!: {_route}'),
        navigator_animation=NavigatorAnimation(NavigatorAnimation.NONE)
    )

    flet_navigator.render(page)  # Render current page.


if __name__ == '__main__':
    ft.app(target=main)
