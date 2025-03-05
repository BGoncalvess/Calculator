import flet as ft

class Icon(ft.Icon):
    def __init__(self, name: str, on_click=None):
        super().__init__()
        self.name = name
        self.on_click = on_click