import flet as ft
from .node_component import NodeComponent


class NodeGridComponent(ft.GridView):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.max_extent = 400
        self.child_aspect_ratio = 3
        self.padding = 2
        self.addNodes(3)

    def addNodes(self, ammount: int = 1):
        for i in range(0, ammount):
            self.controls.append(
                NodeComponent(i)
            )
