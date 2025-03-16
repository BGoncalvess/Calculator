import flet as ft
from core.History import History

class HistoryView(ft.View):
    def __init__(self):
        super().__init__(route="/history")
        self.history = History()

        self.controls = [
            ft.Column(
                controls=[
                    self.history
                ]
            )
        ]

    