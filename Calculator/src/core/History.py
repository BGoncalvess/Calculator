import flet as ft
from logger.LogFormat import LogFormat
from buttons.CloseButton import CloseButton

class History(ft.View):
    def __init__(self,history_data, page):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        
        self.controls=[
            ft.Column(
                controls=[
                    ft.Text("History"),
                    ft.Row(
                        self.show_history(history_data),
                    )
                ]
            ),
            ft.Row(
                controls=[
                    CloseButton(page)
                ]
            )
        ]

    def show_history(self, history_data):
        self.logger.info(f"History data: {history_data}")
        if not history_data:
            return [
                ft.Text(value="No history available", color=ft.colors.BLACK, size=16)
            ]
        else:
            return [ft.Text(value=str(entry), color=ft.colors.BLACK, size=16)
                    for entry in history_data]