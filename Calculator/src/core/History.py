import flet as ft
from logger.LogFormat import LogFormat
from buttons.DownloadButton import DownloadButton
from buttons.CloseButton import CloseButton

class History(ft.View):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.controls = [
            ft.Column(
                controls=[
                    ft.Text(value="History1", color=ft.colors.BLACK, size=20),
                    ft.Text(value="History1", color=ft.colors.BLACK, size=20),
                    ft.Text(value="History1", color=ft.colors.BLACK, size=20)
                ]
            ),
            ft.Column(
                controls=[
                    ft.Container(expand=True),
                    ft.Row(
                        controls=[
                            DownloadButton(),
                            CloseButton()
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                expand=True
            )
        ]
