import flet as ft
from core import Calculator, History
from logger.LogFormat import LogFormat

class RouteManager(ft.RouteChangeEvent):
    def __init__(self, page):
        super().__init__()

        self.dict_views = {
            "Calculator": Calculator(),
            "History" : History()
        }

        self.logger = LogFormat(__name__).logger
        self.page = page
        self.route = self.page.route
        self.route.add_route_change_listener(self.on_route_change)

    def route_change(self, e):
        self.page.view.clear()
        match e.route:
            case "/":
                self.page.views.append()
            case "/history":
                self.page.views.append(self.dict_views["History"])
            case "/calculator":
                self.page.views.append(self.dict_views["Calculator"])
        self.page.update()