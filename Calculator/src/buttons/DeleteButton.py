import flet as ft
from buttons.IconButton import IconButton
from formats.LogFormat import LogFormat

class DeleteButton(IconButton):
    def __init__(self):
        super().__init__(name=ft.icons.DELETE, on_click=self.__on_click_handler)
        self.logger = LogFormat(__name__).logger

    def __on_click_handler(self, e):
        self.logger.info("Delete button clicked")