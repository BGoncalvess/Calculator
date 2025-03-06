import flet as ft
from core import RouteManager

def main(page: ft.Page):
    
    page.title = "Calculator App"
    
    RouteManager.initialize_route_manager(page)

    page.window.width=400
    page.window.height=500
    
ft.app(target=main)