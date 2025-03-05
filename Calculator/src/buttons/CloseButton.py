import flet as ft
from buttons import Button


class CloseButton(ft.Button):
    def __init__(self, page):
        super().__init__(icon="")
        self.page = page
        self.on_click = self.close

    def close(self, e):
        if self.page.views:
            self.page.views.pop()
            self.page.update() 