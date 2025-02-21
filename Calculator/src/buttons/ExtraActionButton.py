import flet as ft
from buttons.Button import Button

class ExtraActionButton(Button):
    def __init__(self, text, button_clicked):
        Button.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK