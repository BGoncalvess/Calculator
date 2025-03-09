import flet as ft
from formats.LogFormat import LogFormat
from buttons.DownloadButton import DownloadButton
from buttons.CloseButton import CloseButton
from buttons.CloseButton import CloseButton
from storage.HistoryStorage import HistoryStorage

class History(ft.Container):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.history_storage = HistoryStorage().get_history()
        self.logger.info(f"History: {self.history_storage}")

        self.history_controls = []
        if self.history_storage:
            for entry in self.history_storage:
                self.history_controls.append(ft.Text(str(entry), color=ft.colors.BLACK, size=20))
        else:
            self.history_controls.append(ft.Text("No history available", color=ft.colors.BLACK, size=20))

        self.content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=self.history_controls
                            ),
                            DownloadButton()
                        ],
                    ),
                    ft.Column(
                        controls=[
                            ft.Container(expand=True),
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
