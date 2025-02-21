import flet as ft
import Calculator as Calculator

def main(page: ft.Page):
    page.title = "Calculator App"

    calc = Calculator.CalculatorApp()

    page.add(calc)


ft.app(target=main)