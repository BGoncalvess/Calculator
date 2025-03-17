import flet as ft
from core.History import History
from views.HistoryContent import HistoryContent

class HistoryView(ft.View):
    def __init__(self):
        super().__init__(route="/history")
        self.history_content = HistoryContent()

        self.controls = [
            self.history_content,  # Add HistoryContent to the view first
        ]

    def did_mount(self):
        self.history_content.update()  # Ensure the history content is updated after mounting