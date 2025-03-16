import flet as ft
from views.HistoryContent import HistoryContent

class History(ft.Container):
    def __init__(self):
        super().__init__()
        self.history_content = HistoryContent()