import itertools
import flet as ft
from board_list import BoardList
from data_store import DataStore
from column_manager import ColumnManager


class Board(ft.Container):
    id_counter = itertools.count()

    def __init__(self, app, store: DataStore, name: str, page: ft.Page):
        print(f"Store type: {type(store).__name__}")

        # if page is None:
        #     print("Warning: Board initialized with None page")

        assert page is not None, "Board requires a valid page instance"
        self.page: ft.Page = page
        self.board_id = next(Board.id_counter)
        print(f"Initializing Board with ID: {self.board_id}")  # Debug print
        self.store: DataStore = store
        self.app = app
        self.name = name
        
        self.add_list_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, text="Add Card", height=30, on_click=self.create_list
        )

        self.add_column_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, text="Add Column", height=30, on_click=self.create_column
        )

        self.manage_labels_button = ft.FloatingActionButton(
            icon=ft.Icons.LABEL, text="Manage Labels", height=30, on_click=self.manage_labels
        )

        self.button_row = ft.Row(
            controls=[self.add_list_button, self.add_column_button, self.manage_labels_button],
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            width=(self.app.page.width - 310),
            height=50,
        )

        self.column_manager = ColumnManager(self.page)  # Pass page to ColumnManager
        self.board_lists = ft.Row(
            controls=self.column_manager.get_columns(),
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            width=(self.app.page.width - 310),
            height=(self.app.page.height - 145),
        )

        for l in self.store.get_lists_by_board(self.board_id):
            if l.page is None:
                l.page = self.page
                print(f"Setting page for stored list ID: {l.board_list_id}")
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
        self.board_lists.height = height - 145
        self.update()

    def manage_labels(self, e):
        def close_dlg(e):
            self.page.close(dialog)

        def search_labels(e):
            search_term = search_field.value.lower()
            filtered_items = [
                item for item in all_items
                if any(label.lower().startswith(search_term) for label in item.labels)
            ]
            update_item_list(filtered_items)

        def update_item_list(items_to_show):
            item_list.controls = []
            for item in items_to_show:
                label_row = ft.Row(
                    [
                        ft.Chip(
                            label=ft.Text(l),
                            bgcolor=item.label_colors.get(l, ft.Colors.BLUE_200)
                        ) for l in item.labels
                    ],
                    wrap=True,
                    scroll=ft.ScrollMode.AUTO,  # Allow horizontal scrolling for many labels
                    width=400,  # Constrain width to fit dialog
                )
                item_list.controls.append(
                    ft.Column([
                        ft.Text(item.item_text),
                        label_row,
                    ])
                )
            self.page.update()

        all_items = []
        for bl in self.store.get_lists_by_board(self.board_id):
            all_items.extend(self.store.get_items(bl.board_list_id))

        # Add label_colors attribute to items if not present
        for item in all_items:
            if not hasattr(item, 'label_colors'):
                item.label_colors = {}  # Dictionary to store label -> color mapping

        search_field = ft.TextField(label="Search Labels", on_change=search_labels)
        item_list = ft.Column([], scroll=ft.ScrollMode.AUTO)

        update_item_list(all_items)

        dialog = ft.AlertDialog(
            title=ft.Text("Manage Labels"),
            content=ft.Column(
                [
                    search_field,
                    item_list,
                ],
                scroll=ft.ScrollMode.AUTO,
                height=500,
                width=600,
            ),
            actions=[ft.ElevatedButton("Close", on_click=close_dlg)],
        )
        self.page.open(dialog)

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
                new_list = BoardList(self, self.store, dialog_text.value, self.page, color=color_options.data)
                print(f"Created new_list ID: {new_list.board_list_id} for board ID: {self.board_id}, page: {new_list.page}")
                if column_selector.value is not None:
                    column_index = int(column_selector.value)
                    if column_index < len(self.board_lists.controls):
                        column = self.board_lists.controls[column_index]
                        if isinstance(column, ft.Column):
                            column.controls[1].controls.append(new_list.view)
                            new_list.column = column
                            self.store.add_list(self.board_id, new_list)
                            self.page.update()
                        else:
                            raise ValueError(f"Column at index {column_index} is not a Column")
                    else:
                        raise ValueError(f"Invalid column index: {column_index}")
                else:
                    if self.board_lists.controls and isinstance(self.board_lists.controls[0], ft.Column):
                        self.board_lists.controls[0].controls[1].controls.append(new_list.view)
                        new_list.column = self.board_lists.controls[0]
                    else:
                        self.board_lists.controls.append(new_list.view)
                    self.store.add_list(self.board_id, new_list)
                    self.page.update()
                print(f"After adding, new_list page: {new_list.page}")
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
        print(f"Removing list with ID: {list.board_list_id} from board ID: {self.board_id}")
        removed = False
        
        # Check columns
        if self.board_lists.controls and isinstance(self.board_lists.controls[0], ft.Column):
            for column in self.board_lists.controls:
                if isinstance(column, ft.Column) and list.view in column.controls[1].controls:
                    column.controls[1].controls.remove(list.view)
                    removed = True
                    break
        
        # Check top-level board_lists.controls (non-column case)
        if not removed and list.view in self.board_lists.controls:
            self.board_lists.controls.remove(list.view)
            removed = True
        
        # Check page.controls (since we added it there)
        if not removed and list.view in self.page.controls:
            self.page.controls.remove(list.view)
            removed = True
        
        if removed:
            self.store.remove_list(self.board_id, list.board_list_id)
            self.page.update()
        else:
            raise ValueError("List not found in board lists")

    def add_list(self, list):
        if self.board_lists.controls and isinstance(self.board_lists.controls[0], ft.Column):
            self.board_lists.controls[0].controls[1].controls.append(list.view)
            list.column = self.board_lists.controls[0]
        else:
            self.board_lists.controls.insert(-1, list.view)
        self.store.add_list(self.board_id, list)
        self.page.update()

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
        new_column = self.column_manager.add_column(column_name, color)
        delete_button = ft.FloatingActionButton(
            icon=ft.Icons.DELETE, text="Remove Column", height=30, on_click=self.delete_column, data=len(self.board_lists.controls)
        )
        edit_button = ft.FloatingActionButton(
            icon=ft.Icons.EDIT, text="Edit Column", height=30, on_click=self.edit_column, data=len(self.board_lists.controls),
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