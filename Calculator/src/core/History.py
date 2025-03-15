import flet as ft
from formats.LogFormat import LogFormat
from buttons.DownloadButton import DownloadButton
from buttons.CloseButton import CloseButton
from storage.HistoryStorage import HistoryStorage

class History(ft.Container):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.history_list = ft.Column()

        self.content = HistoryContent()

class HistoryContent(ft.Column):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.history_list = ft.Column()
        self.controls=[
            ft.Row(
                controls=[
                    ft.Text("Index Date Expression Result", color=ft.colors.BLACK, size=20),
                    self.history_list
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

    def update(self):
        for entry in HistoryStorage.get_history() or []:
            self.history_list.controls.append(
                ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(f"{entry.index} - {entry.date} - {entry.expression} = {entry.result}", color=ft.colors.BLACK, size=20),
                                DownloadButton()
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        return super().update()