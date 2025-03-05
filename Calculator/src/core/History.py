import flet as ft
from logger.LogFormat import LogFormat
from buttons import CloseButton

class History(ft.View):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger