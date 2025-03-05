import flet as ft
from buttons.Icon import Icon
from core import RouteManager
from logger.LogFormat import LogFormat

class HistoryButton(Icon):
    def __init__(self):
        super().__init__(name=ft.icons.HISTORY, on_click=self.on_click)
        self.logger = LogFormat(__name__).logger

    def on_click(self, e):
        self.logger.info("History button clicked")
        RouteManager.route_change("/history")
        self.logger.info("Route changed to History")