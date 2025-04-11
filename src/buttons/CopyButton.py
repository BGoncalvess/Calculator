import flet as ft
from src.buttons.IconButton import IconButton
from src.formats.LogFormat import LogFormat


class CopyButton(IconButton):

    def __init__(self, result):
        super().__init__(name=ft.icons.COPY, on_click=self.__on_click_handler)
        self.logger = LogFormat(__name__).logger
        self.result = result

    def __on_click_handler(self, e):
        self.logger.info(f"Copy button clicked for result: {self.result}")
        self.page.set_clipboard(self.result)
        self.logger.info(f"Copied '{self.result}' to clipboard")
