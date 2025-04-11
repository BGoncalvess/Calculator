import flet as ft
from src.buttons.IconButton import IconButton
from src.formats.LogFormat import LogFormat


class HistoryButton(IconButton):

    def __init__(self):
        super().__init__(name=ft.icons.HISTORY,
                         on_click=self.__on_click_handler)
        self.logger = LogFormat(__name__).logger

    def __on_click_handler(self, e):
        self.logger.info("History button clicked")
        self.page.go("/history")
