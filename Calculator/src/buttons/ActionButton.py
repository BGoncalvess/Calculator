import flet as ft
from buttons import Button 

class ActionButton(Button):
    def __init__(self, text, button_clicked):
        Button.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE