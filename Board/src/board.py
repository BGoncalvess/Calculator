import itertools
import flet as ft
from board_list import BoardList
from data_store import DataStore
from column_manager import ColumnManager


class Board(ft.Container):
    id_counter = itertools.count()

    def __init__(self, app, store: DataStore, name: str, page: ft.Page):
        self.page: ft.Page = page
        self.board_id = next(Board.id_counter)
        self.store: DataStore = store
        self.app = app
        self.name = name
        
        self.add_list_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, text="Add Card", height=30, on_click=self.create_list
        )

        self.add_column_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, text="Add Column", height=30, on_click=self.create_column
        )

        self.button_row = ft.Row(
            controls=[self.add_list_button, self.add_column_button],
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            width=(self.app.page.width - 310),
            height=50,
        )

        self.board_lists = ft.Row(
            controls=[],
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            width=(self.app.page.width - 310),
            height=(self.app.page.height - 145),
        )

        for l in self.store.get_lists_by_board(self.board_id):
            self.add_list(l)

        super().__init__(
            content=ft.Column(
                controls=[self.button_row, self.board_lists],
                expand=True,
            ),
            data=self,
            margin=ft.margin.all(0),
            padding=ft.padding.only(top=10, right=0),
            height=self.app.page.height,
        )

    def resize(self, nav_rail_extended, width, height):
        self.board_lists.width = (width - 310) if nav_rail_extended else (width - 50)
        self.height = height
        self.update()

    def create_list(self, e):
        option_dict = {
            ft.Colors.LIGHT_GREEN: self.color_option_creator(ft.Colors.LIGHT_GREEN),
            ft.Colors.RED_200: self.color_option_creator(ft.Colors.RED_200),
            ft.Colors.AMBER_500: self.color_option_creator(ft.Colors.AMBER_500),
            ft.Colors.PINK_300: self.color_option_creator(ft.Colors.PINK_300),
            ft.Colors.ORANGE_300: self.color_option_creator(ft.Colors.ORANGE_300),
            ft.Colors.LIGHT_BLUE: self.color_option_creator(ft.Colors.LIGHT_BLUE),
            ft.Colors.DEEP_ORANGE_300: self.color_option_creator(ft.Colors.DEEP_ORANGE_300),
            ft.Colors.PURPLE_100: self.color_option_creator(ft.Colors.PURPLE_100),
            ft.Colors.RED_700: self.color_option_creator(ft.Colors.RED_700),
            ft.Colors.TEAL_500: self.color_option_creator(ft.Colors.TEAL_500),
            ft.Colors.YELLOW_400: self.color_option_creator(ft.Colors.YELLOW_400),
            ft.Colors.PURPLE_400: self.color_option_creator(ft.Colors.PURPLE_400),
            ft.Colors.BROWN_300: self.color_option_creator(ft.Colors.BROWN_300),
            ft.Colors.CYAN_500: self.color_option_creator(ft.Colors.CYAN_500),
            ft.Colors.BLUE_GREY_500: self.color_option_creator(ft.Colors.BLUE_GREY_500),
        }

        def set_color(e):
            color_options.data = e.control.data
            for k, v in option_dict.items():
                if k == e.control.data:
                    v.border = ft.border.all(3, ft.Colors.BLACK26)
                else:
                    v.border = None
            dialog.content.update()

        color_options = ft.GridView(runs_count=3, max_extent=40, data="", height=150)

        for _, v in option_dict.items():
            v.on_click = set_color
            color_options.controls.append(v)

        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                type(e.control) is ft.TextField and e.control.value != ""
            ):
                new_list = BoardList(
                    self,
                    self.store,
                    dialog_text.value,
                    self.page,
                    color=color_options.data,
                )
                if column_selector.value is not None:
                    column_index = int(column_selector.value)
                else:
                    column_index = 0  # Default to the first column if no column is selected

                if column_index < len(self.board_lists.controls):
                    column = self.board_lists.controls[column_index]
                    if isinstance(column, ft.Column):
                        column_manager = ColumnManager()
                        column_manager.columns = self.board_lists.controls  # Ensure columns are set
                        column_manager.add_list_to_column(column_index, new_list, self.page)
                        new_list.column = column  # Add reference to the column
                        self.page.update()  # Update the page
                else:
                    self.add_list(new_list)
                    self.page.update()  # Update the page
            self.page.close(dialog)

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        column_options = [
            ft.dropdown.Option(str(i)) for i, control in enumerate(self.board_lists.controls) if isinstance(control, ft.Column)
        ]
        column_selector = ft.Dropdown(
            options=column_options,
            label="Select Column (optional)",
        )

        dialog_text = ft.TextField(
            label="New List Name", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ft.ElevatedButton(
            text="Create", bgcolor=ft.Colors.BLUE_200, on_click=close_dlg, disabled=True
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Name your new list"),
            content=ft.Column(
                [
                    ft.Container(
                        content=dialog_text, padding=ft.padding.symmetric(horizontal=5)
                    ),
                    column_selector,
                    color_options,
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Cancel", on_click=close_dlg),
                            create_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(dialog)
        dialog_text.focus()

    def create_column(self, e):
        option_dict = {
            ft.Colors.LIGHT_GREEN: self.color_option_creator(ft.Colors.LIGHT_GREEN),
            ft.Colors.RED_200: self.color_option_creator(ft.Colors.RED_200),
            ft.Colors.AMBER_500: self.color_option_creator(ft.Colors.AMBER_500),
            ft.Colors.PINK_300: self.color_option_creator(ft.Colors.PINK_300),
            ft.Colors.ORANGE_300: self.color_option_creator(ft.Colors.ORANGE_300),
            ft.Colors.LIGHT_BLUE: self.color_option_creator(ft.Colors.LIGHT_BLUE),
            ft.Colors.DEEP_ORANGE_300: self.color_option_creator(ft.Colors.DEEP_ORANGE_300),
            ft.Colors.PURPLE_100: self.color_option_creator(ft.Colors.PURPLE_100),
            ft.Colors.RED_700: self.color_option_creator(ft.Colors.RED_700),
            ft.Colors.TEAL_500: self.color_option_creator(ft.Colors.TEAL_500),
            ft.Colors.YELLOW_400: self.color_option_creator(ft.Colors.YELLOW_400),
            ft.Colors.PURPLE_400: self.color_option_creator(ft.Colors.PURPLE_400),
            ft.Colors.BROWN_300: self.color_option_creator(ft.Colors.BROWN_300),
            ft.Colors.CYAN_500: self.color_option_creator(ft.Colors.CYAN_500),
            ft.Colors.BLUE_GREY_500: self.color_option_creator(ft.Colors.BLUE_GREY_500),
        }

        def set_color(e):
            color_options.data = e.control.data
            for k, v in option_dict.items():
                if k == e.control.data:
                    v.border = ft.border.all(3, ft.Colors.BLACK26)
                else:
                    v.border = None
            dialog.content.update()

        color_options = ft.GridView(runs_count=3, max_extent=40, data="", height=150)

        for _, v in option_dict.items():
            v.on_click = set_color
            color_options.controls.append(v)

        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                type(e.control) is ft.TextField and e.control.value != ""
            ):
                self.add_column(dialog_text.value, color_options.data)
            self.page.close(dialog)

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        dialog_text = ft.TextField(
            label="New Column Name", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ft.ElevatedButton(
            text="Create", bgcolor=ft.Colors.BLUE_200, on_click=close_dlg, disabled=True
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Name your new column"),
            content=ft.Column(
                [
                    ft.Container(
                        content=dialog_text, padding=ft.padding.symmetric(horizontal=5)
                    ),
                    color_options,
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Cancel", on_click=close_dlg),
                            create_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(dialog)
        dialog_text.focus()
        
    def remove_list(self, list: BoardList, e):
        for column in self.board_lists.controls:
            if isinstance(column, ft.Column):
                if list in column.controls[1].controls:
                    column.controls[1].controls.remove(list)
                    self.store.remove_list(self.board_id, list.board_list_id)
                    self.page.update()
                    return
            elif list in self.board_lists.controls:
                self.board_lists.controls.remove(list)
                self.store.remove_list(self.board_id, list.board_list_id)
                self.page.update()
                return
        raise ValueError("List not found in board lists")

    def add_list(self, list):
        self.board_lists.controls.insert(-1, list)
        self.store.add_list(self.board_id, list)
        self.page.update()  # Update the page

    def color_option_creator(self, color: str):
        return ft.Container(
            bgcolor=color,
            border_radius=ft.border_radius.all(50),
            height=10,
            width=10,
            padding=ft.padding.all(5),
            alignment=ft.alignment.center,
            data=color,
        )

    def add_column(self, column_name: str, color: str):
        column_manager = ColumnManager()
        new_column = column_manager.add_column(column_name, color)
        delete_button = ft.FloatingActionButton(
            icon=ft.Icons.DELETE, text="Remove Column", height=30, on_click=self.delete_column, data=len(self.board_lists.controls)
        )
        edit_button = ft.FloatingActionButton(
            icon=ft.Icons.EDIT, text="Edit Column", height=30, on_click=self.edit_column, data=len(self.board_lists.controls)
        )
        new_column.controls.append(delete_button)
        new_column.controls.append(edit_button)
        self.board_lists.controls.append(new_column)
        self.page.update()

    def edit_column(self, e):
        column_index = e.control.data
        if (column_index < len(self.board_lists.controls)):
            column = self.board_lists.controls[column_index]

            def close_dlg(e):
                if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                    type(e.control) is ft.TextField and e.control.value != ""
                ):
                    column.controls[0].content.controls[0].value = dialog_text.value
                    self.page.update()
                self.page.close(dialog)

            def textfield_change(e):
                if dialog_text.value == "":
                    create_button.disabled = True
                else:
                    create_button.disabled = False
                self.page.update()

            dialog_text = ft.TextField(
                label="Edit Column Name", value=column.controls[0].content.controls[0].value, on_submit=close_dlg, on_change=textfield_change
            )
            create_button = ft.ElevatedButton(
                text="Save", bgcolor=ft.Colors.BLUE_200, on_click=close_dlg, disabled=True
            )
            dialog = ft.AlertDialog(
                title=ft.Text("Edit your column"),
                content=ft.Column(
                    [
                        ft.Container(
                            content=dialog_text, padding=ft.padding.symmetric(horizontal=5)
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(text="Cancel", on_click=close_dlg),
                                create_button,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    tight=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )
            self.page.open(dialog)
            dialog_text.focus()
        
    def delete_column(self, e):
        column_index = e.control.data
        if column_index < len(self.board_lists.controls):
            del self.board_lists.controls[column_index]
            self.page.update()