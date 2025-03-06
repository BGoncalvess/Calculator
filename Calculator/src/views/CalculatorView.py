import flet as ft
from core.Calculator import Calculator

class CalculatorView(ft.View):
    def __init__(self):
        super().__init__()
        self.controls = [
            ft.Column(
                controls=[
                    Calculator()
                ]
            )
        ]