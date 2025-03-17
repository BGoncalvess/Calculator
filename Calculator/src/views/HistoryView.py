import flet as ft
from core.History import History
from views.HistoryContent import HistoryContent

class HistoryView(ft.View):
    def __init__(self):
        super().__init__(route="/history")
        self.history_content = HistoryContent()

        self.controls = [
            self.history_content,
        ]

    def did_mount(self):
        # Explicitly set the page for HistoryContent
        self.history_content.page = self.page
        # Update HistoryContent after the view is mounted
        self.history_content.update()