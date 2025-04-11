import flet as ft
from src.views.HistoryContent import HistoryContent


class History(ft.Container):

    def __init__(self):
        super().__init__()
        self.history_content = HistoryContent()
        self.content = self.history_content
