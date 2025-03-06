import flet as ft
from buttons.IconButton import IconButton
from logger.LogFormat import LogFormat

class HistoryButton(IconButton):
    def __init__(self):
        super().__init__(name=ft.icons.HISTORY, on_click=self.__on_click_handler)
        self.logger = LogFormat(__name__).logger

    def __on_click_handler(self, e):
        self.logger.info("History button clicked")
        self.logger.info("Route changed to /history")
        self.page.go("/history")
        self.page.update()