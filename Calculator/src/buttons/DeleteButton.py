import flet as ft
from buttons.IconButton import IconButton
from formats.LogFormat import LogFormat

class DeleteButton(IconButton):
    def __init__(self, history_index):
        super().__init__(name=ft.icons.DELETE, on_click=self.__on_click_handler)
        self.logger = LogFormat(__name__).logger
        self.history_index = history_index

    def __on_click_handler(self, e):
        from storage.HistoryStorage import HistoryStorage
        from core.RouteManager import RouteManager
        self.logger.info(f"Delete button clicked for history index: {self.history_index}")
        HistoryStorage.remove_history(self.history_index)
        history_view = RouteManager.get().dict_views["History"]
        history_view.history_content.update()
        history_view.page.update()