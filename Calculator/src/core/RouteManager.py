import flet as ft
from views.CalculatorView import CalculatorView
from views.HistoryView import HistoryView
from formats.LogFormat import LogFormat

class RouteManager():
    instance = None

    def __init__(self, page:ft.Page):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.page = page
        self.dict_views = {
            "Calculator": CalculatorView(),
            "History" : HistoryView()
        }

        self.page.on_route_change = self.route_change
        self.page.go("/")
        self.page.update()
        
    async def route_change(self, e:ft.RouteChangeEvent):
        self.logger.info(f"Route changed to {e.route}") 
        self.page.views.clear()
        match e.route:
            case "/":
                self.page.views.append(self.dict_views["Calculator"])
            case "/history":
                self.page.views.append(self.dict_views["Calculator"])
                self.page.views.append(self.dict_views["History"])

        self.page.update()

    def view_pop(self):
        self.page.route = self.page.views[-2].route
        self.page.update()

    @classmethod
    def initialize_route_manager(cls, page:ft.Page) -> 'RouteManager':
        if cls.instance is None:
            cls.instance = cls(page)
        return cls.instance

    @classmethod
    def get(cls) -> 'RouteManager':
        if cls.instance is None:
            raise Exception("RouteManager not initialized")
        return cls.instance
