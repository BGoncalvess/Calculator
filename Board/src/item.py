from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board_list import BoardList
import itertools
import flet as ft
from data_store import DataStore


class Item(ft.Container):
    id_counter = itertools.count()

    def __init__(self, list: "BoardList", store: DataStore, item_text: str):
        self.item_id = next(Item.id_counter)
        self.store: DataStore = store
        self.list = list
        self.item_text = item_text
        # Initialize labels and label_colors from store or as empty
        existing_item = next((i for i in self.store.get_items(self.list.board_list_id) if i.item_id == self.item_id), None)
        self.labels = existing_item.labels if existing_item else []
        self.label_colors = existing_item.label_colors if existing_item else {}

        print(f"Initialized item {self.item_id} with labels {self.labels} and colors {self.label_colors}")

        self.add_label_button = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            tooltip="Add Label",
            on_click=self.add_label_dialog,
        )

        self.card_item = ft.Card(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Checkbox(label=f"{self.item_text}", width=200),
                                self.build_labels_row(),  # Dynamic label row
                            ]
                        ),
                        border_radius=ft.border_radius.all(5),
                    ),
                    self.add_label_button,
                ],
                width=250,
                wrap=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            elevation=1,
            data=self  # Optional, keep if needed elsewhere
        )

        self.view = ft.Draggable(
            group="items",
            content=ft.DragTarget(
                group="items",
                content=self.card_item,
                on_accept=self.drag_accept,
                on_leave=self.drag_leave,
                on_will_accept=self.drag_will_accept,
                # Remove data=self from DragTarget unless needed for other logic
            ),
            data=self  # Set data on Draggable
        )

        uid=f"item_{self.item_id}"
        print("uid", uid)

        super().__init__(content=self.view)

        if not existing_item:
            self.store.add_item(self.list.board_list_id, self)

    def drag_accept(self, e):
        print(f"e.src_id: {e.src_id}")
        src = self.page.get_control(e.src_id)
        if src is None:
            print("src is None - Control not found on page")
            return
        if src.data is None:
            print("src.data is None - No data associated with dragged control")
            return
        if not isinstance(src.data, Item):
            print(f"Unexpected src.data type: {type(src.data).__name__}")
            return

        # Skip if item is dropped on itself
        if src.content.content == e.control.content:
            self.card_item.elevation = 1
            self.list.set_indicator_opacity(self, 0.0)
            e.control.update()
            return

        src_item = src.data  # The original item being dragged
        src_list = src_item.list  # The source list
        target_list = self.list  # The target list

        # If item is dropped within the same list
        if src_list == target_list:
            self.list.add_item(chosen_control=src_item, swap_control=self)
            self.card_item.elevation = 1
            e.control.update()
            return

        # Item dropped into a different list
        # Remove from source list
        src_list.remove_item(src_item)

        # Add the original item to the target list at the swap position
        target_list.add_item(item=None, chosen_control=src_item, swap_control=self)

        # Update the item's list reference
        src_item.list = target_list

        # Reset UI states
        self.list.set_indicator_opacity(self, 0.0)
        self.card_item.elevation = 1
        self.card_item.update()
        self.page.update()
        print(f"Moved item {src_item.item_id} from list {src_list.board_list_id} to {target_list.board_list_id} with labels {src_item.labels}")

    def drag_will_accept(self, e):
        if e.data == "true":
            self.list.set_indicator_opacity(self, 1.0)
        self.card_item.elevation = 20 if e.data == "true" else 1
        self.page.update()

    def drag_leave(self, e):
        self.list.set_indicator_opacity(self, 0.0)
        self.card_item.elevation = 1
        self.page.update()

    def add_label_dialog(self, e):
        def close_dlg(e):
            if label_text.value and color_options.data:
                new_label = label_text.value
                if new_label not in self.labels:
                    self.labels.append(new_label)
                    self.label_colors[new_label] = color_options.data
                    print(f"Adding label {new_label} with color {color_options.data} to item {self.item_id}")
                    self.store.update_item_labels(self.list.board.board_id, self.item_id, self.labels)
                    self.update_card_content()
                self.page.close(dialog)

        def textfield_change(e):
            create_button.disabled = not label_text.value
            self.page.update()

        label_text = ft.TextField(label="New Label Name", on_change=textfield_change)
        color_options = ft.GridView(runs_count=3, max_extent=40, data=ft.Colors.BLUE_200, height=200)
        
        color_dict = {        
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
            for k, v in color_dict.items():
                v.border = ft.border.all(3, ft.Colors.BLACK26) if k == e.control.data else None
            dialog.content.update()

        for v in color_dict.values():
            v.on_click = set_color
            color_options.controls.append(v)

        create_button = ft.ElevatedButton(text="Add", on_click=close_dlg, disabled=True)
        dialog = ft.AlertDialog(
            title=ft.Text("Add Label"),
            content=ft.Column([label_text, color_options, create_button], tight=True),
            on_dismiss=lambda e: print("Dialog dismissed"),
        )
        self.page.open(dialog)
        label_text.focus()

    def update_card_content(self):
        print(f"Updating card for item {self.item_id} with labels {self.labels} and colors {self.label_colors}")
        self.card_item.content = ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Checkbox(label=f"{self.item_text}", width=200),
                            self.build_labels_row(),
                        ]
                    ),
                    border_radius=ft.border_radius.all(5),
                ),
                self.add_label_button,
            ],
            width=250,
            wrap=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self.card_item.update()
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

    def build_labels_row(self):
        return ft.Row(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                l,
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                width=70,  # Fixed width for text
                                overflow=ft.TextOverflow.ELLIPSIS,  # Truncate long text
                            ),
                        ],
                        tight=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=self.label_colors.get(l, ft.Colors.BLUE_200),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=ft.border_radius.all(5),
                    border=ft.border.all(1, ft.Colors.BLACK12),
                    width=100,  # Fixed container width
                    on_click=lambda e, label=l: self.edit_label_dialog(label),
                    ink=True,
                ) for l in self.labels
            ],
            wrap=True,
            spacing=5,
        )
    
    def edit_label_dialog(self, label):
        def save_changes(e):
            new_text = label_text.value
            new_color = color_options.data
            if new_text and new_text != label:
                self.labels[self.labels.index(label)] = new_text
                del self.label_colors[label]
                self.label_colors[new_text] = new_color
            elif new_color != self.label_colors[label]:
                self.label_colors[label] = new_color
            self.store.update_item_labels(self.list.board.board_id, self.item_id, self.labels)
            self.update_card_content()
            self.page.close(dialog)

        def remove_and_close(e):
            self.remove_label(label)
            self.page.close(dialog)

        label_text = ft.TextField(label="Edit Label Name", value=label)
        color_options = ft.GridView(runs_count=3, max_extent=40, data=self.label_colors.get(label, ft.Colors.BLUE_200), height=200)
        color_dict = {
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
            for k, v in color_dict.items():
                v.border = ft.border.all(3, ft.Colors.BLACK26) if k == e.control.data else None
            dialog.content.update()

        for v in color_dict.values():
            v.on_click = set_color
            color_options.controls.append(v)

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Label"),
            content=ft.Column([label_text, color_options], tight=True),
            actions=[
                ft.ElevatedButton("Save", on_click=save_changes),
                ft.ElevatedButton("Remove Label", on_click=remove_and_close),
                ft.ElevatedButton("Cancel", on_click=lambda e: self.page.close(dialog))
            ],
        )
        self.page.open(dialog)
        label_text.focus()

    def remove_label(self, label):
        if label in self.labels:
            self.labels.remove(label)
            del self.label_colors[label]
            self.store.update_item_labels(self.list.board.board_id, self.item_id, self.labels)
            self.update_card_content()