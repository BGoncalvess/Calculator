import flet as ft
from src.core import RouteManager
from src.storage.HistoryStorage import HistoryStorage


def main(page: ft.Page):

    page.title = "Calculator App"

    HistoryStorage.initialize(page)
    RouteManager.initialize_route_manager(page)

    page.window.width = 400
    page.window.height = 500


ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="./src/assets")

# ft.app(target=main)
