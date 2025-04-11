import flet as ft
from src.core.History import History
from src.views.HistoryContent import HistoryContent


class HistoryView(ft.View):

    def __init__(self):
        super().__init__(route="/history")
        self.width = 350
        self.padding = 20
        self.history_content = HistoryContent()
        self.controls = [
            self.history_content,
        ]

    def did_mount(self):
        self.history_content.page = self.page
        self.history_content.update()
