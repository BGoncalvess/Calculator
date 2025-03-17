import flet as ft
from formats.LogFormat import LogFormat
from buttons.CopyButton import CopyButton
from buttons.CloseButton import CloseButton
from buttons.DeleteButton import DeleteButton
from storage.HistoryStorage import HistoryStorage

class HistoryContent(ft.Column):
    def __init__(self):
        super().__init__(expand=True,spacing=10)
        self.logger = LogFormat(__name__).logger
        self.history_list = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Index")),
                ft.DataColumn(label=ft.Text("Date")),
                ft.DataColumn(label=ft.Text("Expression")),
                ft.DataColumn(label=ft.Text("Result")),
                ft.DataColumn(label=ft.Text("Actions")),
            ],
            expand=True,
            column_spacing=5,
            heading_row_height=40,
            data_row_min_height=40,
            data_row_max_height=60,
        )
        self.controls = [
            ft.Row(
                controls=[
                    ft.Container(expand=True),
                    CloseButton()
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[self.history_list],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=True,
                padding=10,
            ),
        ]

    def update(self):
        self.logger.info("Updating HistoryContent")
        self.history_list.rows.clear()
        for entry in reversed(HistoryStorage.get_history() or []):
            self.logger.info(f"Adding history entry: {entry.index}, {entry.expression}, {entry.result}")
            self.history_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{entry.index}")),
                        ft.DataCell(ft.Text(f"{entry.date}")),
                        ft.DataCell(ft.Text(f"{entry.expression}")),
                        ft.DataCell(ft.Text(f"{entry.result}")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    DeleteButton(history_index=entry.index),
                                    CopyButton(result=entry.result)
                                ],
                                spacing=5,
                            )
                        ),
                    ]
                )
            )
        super().update()  # Call the parent update method