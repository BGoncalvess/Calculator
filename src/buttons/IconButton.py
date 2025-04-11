import flet as ft

class IconButton(ft.IconButton):
    def __init__(self, name: str, on_click=None):
        super().__init__(icon=name, on_click=on_click)
        