import flet as ft
from core import RouteManager
from storage.HistoryStorage import HistoryStorage

def main(page: ft.Page):
    
    page.title = "Calculator App"
    
    HistoryStorage.initialize(page)
    RouteManager.initialize_route_manager(page)

    page.window.width=400
    page.window.height=500
    
ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=8080)