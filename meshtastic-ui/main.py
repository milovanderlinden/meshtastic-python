import flet as ft


def main(page: ft.Page):
    black_logo = """
<svg width="100%" height="100%" viewBox="0 0 100 55" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(0.802386,0,0,0.460028,-421.748,-122.127)">
        <g transform="matrix(0.579082,0,0,1.01004,460.975,-39.6867)">
            <path d="M250.908,330.267L193.126,415.005L180.938,406.694L244.802,313.037C246.174,311.024 248.453,309.819 250.889,309.816C253.326,309.814 255.606,311.015 256.982,313.026L320.994,406.536L308.821,414.869L250.908,330.267Z"/>
        </g>
        <g transform="matrix(0.582378,0,0,1.01579,485.019,-211.182)">
            <path d="M87.642,581.398L154.757,482.977L142.638,474.713L75.523,573.134L87.642,581.398Z"/>
        </g>
    </g>
</svg>
    """
    page.appbar = ft.AppBar(
        leading=ft.Image(
            src=black_logo,
            width=100,
            height=100,
        ),
        leading_width=40,
        title=ft.Text("Meshtastic"),
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

    floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, bgcolor="#67ea94", foreground_color="#000000"
    )

    # Settings
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.HIDDEN

    # Render components
    page.add(ft.Text("Not connected, select radio below"), cg, navigation_bar, floating_action_button)


ft.app(target=main)
