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
            icon=ft.Icons.ADD, text="Add List", height=30, on_click=self.create_list
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

        self.column_manager = ColumnManager(self.page, self)  # Pass self to ColumnManager
        self.board_lists = ft.Row(
            controls=self.column_manager.get_columns(),
            vertical_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            width=(self.app.page.width - 310),
            height=(self.app.page.height - 145),
        )

        columns = self.column_manager.get_columns()

        for col in columns:
            drag_target = ft.DragTarget(
                group="lists",
                content=col.lists_container,
                on_accept=lambda e, c=col: self.accept_list_to_column(e, c),
                on_will_accept=lambda e, c=col: self.highlight_column(c, True),
                on_leave=lambda e, c=col: self.highlight_column(c, False),
            )
            col.controls[1] = drag_target  # Replace the container with the DragTarget

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
            print(f"Searching for: '{search_term}'")
            if not search_term:  # If search field is empty, show all lists
                update_table(all_lists)
            else:
                filtered_lists = [
                    bl for bl in all_lists
                    if search_term in bl.title.lower() or
                    any(search_term in label.lower() for item in self.store.get_items(bl.board_list_id) for label in item.labels)
                ]
                print(f"Filtered lists: {[bl.title for bl in filtered_lists]}")
                update_table(filtered_lists)

        def update_table(lists_to_show):
            table.rows.clear()  # Clear existing rows
            print("Updating table with lists and their items' labels:")
            seen_labels = set()
            for bl in lists_to_show:
                # Safely extract the column name
                if bl.column and isinstance(bl.column.controls[0].content, ft.Text):
                    column_name = bl.column.controls[0].content.value
                else:
                    column_name = bl.column.controls[0].content.controls[0].value
                
                print(f"List ID {bl.board_list_id}: {bl.title} (Column: {column_name})")
                label_color_map = {}
                for item in self.store.get_items(bl.board_list_id):
                    for label in item.labels:
                        label_color_map[label] = item.label_colors.get(label, ft.Colors.BLUE_200)
                        print(f"  Item {item.item_id}: Label: {label}, Color: {label_color_map[label]}")
                for label, color in label_color_map.items():
                    list_label_key = (bl.board_list_id, label)
                    if list_label_key not in seen_labels:
                        seen_labels.add(list_label_key)
                        table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(column_name)),
                                ft.DataCell(ft.Text(bl.title)),
                                ft.DataCell(ft.Text(label)),
                                ft.DataCell(ft.Text(str(color))),
                            ])
                        )
            # Only call update() if the table is already on the page
            if table.page is not None:
                table.update()
                self.page.update()

        # Collect all BoardLists for this board
        all_lists = self.store.get_lists_by_board(self.board_id)
        print(f"Found {len(all_lists)} lists for board ID {self.board_id}")

        # Ensure all items have labels and label_colors attributes
        for bl in all_lists:
            for item in self.store.get_items(bl.board_list_id):
                if not hasattr(item, 'labels'):
                    item.labels = []
                if not hasattr(item, 'label_colors'):
                    item.label_colors = {}

        search_field = ft.TextField(label="Search Lists or Labels", on_change=search_labels)
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Column")),
                ft.DataColumn(ft.Text("List")),
                ft.DataColumn(ft.Text("Label")),
                ft.DataColumn(ft.Text("Color")),
            ],
            rows=[],
            column_spacing=20,
            heading_row_height=40,
        )

        # Populate table initially without updating (since it’s not on the page yet)
        update_table(all_lists)

        dialog = ft.AlertDialog(
            title=ft.Text("Manage Labels"),
            content=ft.Column(
                [
                    search_field,
                    ft.Column([table], scroll=ft.ScrollMode.AUTO, height=400, width=600),
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
            # Check if the dialog should proceed (e.g., not canceled and text provided)
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                type(e.control) is ft.TextField and e.control.value != ""
            ):
                # Create a new list object
                new_list = BoardList(self, self.store, dialog_text.value, self.page, color=color_options.data)

                # Case 1: A specific column is selected
                if column_selector.value is not None:
                    column_index = int(column_selector.value) - 1
                    if column_index < len(self.board_lists.controls):
                        column = self.board_lists.controls[column_index]
                        if isinstance(column, ft.Column) and len(column.controls) > 1:
                            drag_target = column.controls[1]
                            if isinstance(drag_target, ft.DragTarget):
                                # Append to the DragTarget's content controls
                                drag_target.content.controls.append(new_list.view)
                                new_list.column = column
                                self.store.add_list(self.board_id, new_list)
                                self.page.update()
                            else:
                                raise ValueError("Expected a DragTarget at column.controls[1]")
                        else:
                            raise ValueError(f"Column at index {column_index} is not a valid Column")
                    else:
                        raise ValueError(f"Invalid column index: {column_index}")
                
                # Case 2: No column selected, use default (first) column or create one
                else:
                    if self.board_lists.controls:
                        first_column = self.board_lists.controls[0]
                        if (isinstance(first_column, ft.Column) and 
                            len(first_column.controls) > 1 and 
                            isinstance(first_column.controls[1], ft.DragTarget)):
                            # Append to the DragTarget's content controls
                            first_column.controls[1].content.controls.append(new_list.view)
                            new_list.column = first_column
                        else:
                            raise ValueError("Unexpected structure in first column")
                    else:
                        # Create a default column if none exist
                        delete_button = ft.FloatingActionButton(
                            icon=ft.Icons.DELETE, text="Remove Column", height=30, on_click=self.delete_column, data=len(self.board_lists.controls)
                        )
                        edit_button = ft.FloatingActionButton(
                            icon=ft.Icons.EDIT, text="Edit Column", height=30, on_click=self.edit_column, data=len(self.board_lists.controls),
                        )
                        default_column = ft.Column(
                            controls=[
                                ft.Container(content=ft.Text("Default Column", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER), bgcolor=color_options.data, padding=ft.padding.all(5)),
                                ft.DragTarget(
                                    group="lists",
                                    content=ft.Column(controls=[])
                                ),
                                delete_button,
                                edit_button
                            ]
                        )
                        self.board_lists.controls.append(default_column)
                        default_column.controls[1].content.controls.append(new_list.view)
                        new_list.column = default_column
                    self.store.add_list(self.board_id, new_list)
                    self.page.update()
            
            self.page.close(dialog)

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        column_options = [
            ft.dropdown.Option(str(i + 1)) for i, control in enumerate(self.board_lists.controls) if isinstance(control, ft.Column)
        ]
        column_selector = ft.Dropdown(
            options=column_options,
            label="Select Column",
            width=229,
        )

        dialog_text = ft.TextField(
            label="New List Name", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ft.ElevatedButton(
            text="Create", on_click=close_dlg, disabled=True
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
            text="Create", on_click=close_dlg, disabled=True
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
        
        # Remove from UI
        if self.board_lists.controls and isinstance(self.board_lists.controls[0], ft.Column):
            for column in self.board_lists.controls:
                if isinstance(column, ft.Column) and list.view in column.controls[1].content.controls:
                    column.controls[1].content.controls.remove(list.view)
                    removed = True
                    break
        if not removed and list.view in self.board_lists.controls:
            self.board_lists.controls.remove(list.view)
            removed = True
        if not removed and list.view in self.page.controls:
            self.page.controls.remove(list.view)
            removed = True
        
        # Remove from store
        if removed:
            self.store.remove_list(self.board_id, list.board_list_id)
            # Clean up items associated with this list
            if list.board_list_id in self.store.items:
                del self.store.items[list.board_list_id]
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
                text="Save", on_click=close_dlg, disabled=True
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
            column = self.board_lists.controls[column_index]
            # Remove all lists in this column from the store
            if isinstance(column, ft.Column):
                for control in column.controls[1].content.controls:
                    if isinstance(control, ft.DragTarget) and hasattr(control, 'data'):
                        list_obj = control.data
                        print(f"Removing list ID {list_obj.board_list_id} from store due to column deletion")
                        self.store.remove_list(self.board_id, list_obj.board_list_id)
                        if list_obj.board_list_id in self.store.items:
                            del self.store.items[list_obj.board_list_id]
            del self.board_lists.controls[column_index]
            self.page.update()

    def accept_list_to_column(self, e, target_column):
        src = self.page.get_control(e.src_id)
        if src is None:
            print("src is None - Control not found on page")
            return
        src_list = src.data
        if not isinstance(src_list, BoardList):  # Adjust BoardList to your actual list class
            print(f"Expected BoardList, got {type(src_list).__name__}")
            return
        # Remove from current column
        if src_list.column:
            src_list.column.controls[1].content.controls.remove(src_list.view)
            src_list.column.controls[1].update()
        # Add to target column
        target_column.controls[1].content.controls.append(src_list.view)
        src_list.column = target_column
        target_column.controls[1].update()
        self.page.update()
        print(f"Moved list {src_list.board_list_id} to column {target_column.controls[0].content.controls[0].value}")

    def highlight_column(self, column, highlight):
        container = column.controls[1].content
        if highlight:
            container.border = ft.border.all(2, ft.Colors.BLUE)
        else:
            container.border = None
        container.update()