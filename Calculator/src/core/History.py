import flet as ft
from logger.LogFormat import LogFormat
from buttons.DownloadButton import DownloadButton
from buttons.CloseButton import CloseButton

class History(ft.Container):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(value="History", color=ft.colors.BLACK, size=20),
                        DownloadButton()
                    ]
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                CloseButton()
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    expand=True
                )
            ]
        )
        
    # Expression most recent on top of the history

    # Each element of the list must have
        # - Indice (auto increment)
        # - Data e Hora do calculo
        # - Expressão numerica
        # - Resultado
        # - Delete Button
        # - Copy Button