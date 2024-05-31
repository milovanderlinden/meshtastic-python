import flet as ft
from .node_component import NodeComponent


class NodeGridComponent(ft.GridView):
    def __init__(self):
        super().__init__()
        self.height = 1000,
        self.width = 1000,
        self.runs_count = 5,
        self.max_extent = 150,
        self.child_aspect_ratio = 1.0,
        self.spacing = 5,
        self.run_spacing = 5,

    def addNodes(self, ammount: int = 1):
        for i in range(0, ammount):
            self.controls.append(
                ft.Image(
                    src=f"https://picsum.photos/150/150?{i}",
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                )
            )
            # self.controls.append(NodeComponent(i))
