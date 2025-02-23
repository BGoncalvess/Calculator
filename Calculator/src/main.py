import flet as ft
from core.Calculator import Calculator

def main(page: ft.Page):
    
    page.title = "Calculator App"

    calc = Calculator(page=page)

    page.add(calc)

ft.app(target=main)