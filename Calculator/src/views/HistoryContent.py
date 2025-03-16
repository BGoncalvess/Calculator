import flet as ft
from formats.LogFormat import LogFormat
from buttons.CopyButton import CopyButton
from buttons.CloseButton import CloseButton
from buttons.DeleteButton import DeleteButton
from storage.HistoryStorage import HistoryStorage

class HistoryContent(ft.Column):
    def __init__(self):
        super().__init__(width=400,height=500)
        self.logger = LogFormat(__name__).logger
        self.history_list = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Index")),
                ft.DataColumn(label=ft.Text("Date")),
                ft.DataColumn(label=ft.Text("Expression")),
                ft.DataColumn(label=ft.Text("Result")),
            ],
            rows=[],
        )
        self.controls = [
            self.history_list,
            CloseButton(),
            ft.Column(
                controls=[
                    ft.Container(expand=True),
                    ft.Row(
                        controls=[],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                expand=True
            )
        ]

    def update(self):
        self.history_list.rows.clear()
        for entry in HistoryStorage().get_history() or []:
            self.history_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{entry.index}")),
                        ft.DataCell(ft.Text(f"{entry.date}")),
                        ft.DataCell(ft.Text(f"{entry.expression}")),
                        ft.DataCell(ft.Text(f"{entry.result}")),
                        ft.DataCell(DeleteButton()),
                        ft.DataCell(CopyButton()),
                    ]
                )
            )
        return super().update()