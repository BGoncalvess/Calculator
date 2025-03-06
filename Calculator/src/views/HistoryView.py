import flet as ft
from core.History import History

class HistoryView(ft.View):
    def __init__(self):
        super().__init__()
        self.controls = [
            ft.Column(
                controls=[
                    History()
                ]
            )
        ]