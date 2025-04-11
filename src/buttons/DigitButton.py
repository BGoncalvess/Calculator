import flet as ft
from src.buttons import Button 

class DigitButton(Button):
    def __init__(self, text, button_clicked, expand=1):
        Button.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE