import flet as ft
from core import RouteManager

def main(page: ft.Page):
    
    page.title = "Calculator App"
    
    route_manager : RouteManager = RouteManager(page)

    page.window.width=500
    
    page.add(route_manager)

ft.app(target=main)