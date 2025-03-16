import flet as ft
from buttons.IconButton import IconButton
from formats.LogFormat import LogFormat

class DownloadButton(IconButton):
    def __init__(self):
        super().__init__(name=ft.icons.DOWNLOAD_ROUNDED, on_click=self.__on_click_handler)
        self.logger = LogFormat(__name__).logger

    def __on_click_handler(self, e):
        self.logger.info("Download button clicked")
        # self.page.download("history.txt", "History1\nHistory2\nHistory3")