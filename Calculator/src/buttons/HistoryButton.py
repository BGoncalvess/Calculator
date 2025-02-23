import flet as ft

class HistoryButton(ft.IconButton):
    def __init__(self, on_click=None):
        super().__init__(icon = ft.icons.HISTORY, on_click=on_click)