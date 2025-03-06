import flet as ft
from buttons.IconButton import IconButton
from logger.LogFormat import LogFormat


class CloseButton(IconButton):
    def __init__(self):
        super().__init__(name=ft.icons.CLOSE, on_click=self.__on_click_handler)
        self.logger = LogFormat(__name__).logger

    def __on_click_handler(self, e):
        self.logger.info("Close button clicked")
        from core.RouteManager import RouteManager
        RouteManager.get().view_pop()

