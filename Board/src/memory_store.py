from typing import TYPE_CHECKING
import flet as ft

if TYPE_CHECKING:
    from board import Board
    from board_list import BoardList
    from user import User
    from item import Item

from data_store import DataStore


class InMemoryStore(DataStore):
    def __init__(self):
        self.boards: dict[int, "Board"] = {}
        self.users: dict[str, "User"] = {}
        self.board_lists: dict[int, list["BoardList"]] = {}
        self.items: dict[int, list["Item"]] = {}

    def add_board(self, board: "Board"):
        self.boards[board.board_id] = board
        if board.board_id not in self.board_lists:
            self.board_lists[board.board_id] = []  # Ensure board_lists entry is created
        print(f"Board added with ID: {board.board_id}")  # Debug print

    def get_board(self, id: int):
        return self.boards[id]

    def update_board(self, board: "Board", update: dict):
        for k in update:
            setattr(board, k, update[k])

    def get_boards(self):
        return [self.boards[b] for b in self.boards]

    def remove_board(self, board: "Board"):
        if board.board_id in self.boards:
            del self.boards[board.board_id]
            if board.board_id in self.board_lists:
                del self.board_lists[board.board_id]  # Ensure board_lists entry is removed
            print(f"Board removed with ID: {board.board_id}")  # Debug print
        else:
            raise KeyError(f"Board ID {board.board_id} not found")

    def add_list(self, board: int, list: "BoardList"):
        if board in self.board_lists:
            self.board_lists[board].append(list)
        else:
            self.board_lists[board] = [list]
        print(f"Stored BoardList ID: {list.board_list_id} for board ID: {board}, page: {list.page}")

    def get_lists_by_board(self, board: int):
        return self.board_lists.get(board, [])

    def remove_list(self, board_id, list_id):
        print(f"Removing list with ID: {list_id} from board ID: {board_id}")
        if board_id in self.board_lists:
            self.board_lists[board_id] = [
                l for l in self.board_lists[board_id] if l.board_list_id != list_id
            ]
            if not self.board_lists[board_id]:  # If no lists remain, remove the board_id entry
                del self.board_lists[board_id]
        else:
            raise KeyError(f"Board ID {board_id} not found")

    def add_user(self, user: "User"):
        self.users[user.name] = user

    def get_users(self):
        return [self.users[u] for u in self.users]

    def add_item(self, board_list: int, item: "Item"):
        print(f"Store adding item {item.item_id} to list {board_list}")
        if board_list not in self.items:
            self.items[board_list] = []
        self.items[board_list].append(item)
        print(f"Added item {item.item_id} to list {board_list} with labels {item.labels} and colors {item.label_colors}")

    def get_items(self, board_list: int):
        return self.items.get(board_list, [])

    def remove_item(self, board_list: int, id: int):
        if board_list in self.items:
            self.items[board_list] = [i for i in self.items[board_list] if i.item_id != id]
            print(f"Removed item {id} from list {board_list}")
        else:
            print(f"Warning: List {board_list} not found in store during remove_item")

    def update_item_labels(self, board_id: int, item_id: int, labels: list[str]) -> None:
        for board_list_id in self.items:
            for item in self.items[board_list_id]:
                if item.item_id == item_id:
                    # Preserve existing colors, only update labels
                    old_label_colors = item.label_colors.copy()
                    item.labels = labels
                    # Only set colors for new labels not in old_label_colors
                    item.label_colors = {label: old_label_colors.get(label, ft.Colors.BLUE_200) for label in labels}
                    print(f"Updated item {item_id} in list {board_list_id} with labels {item.labels} and colors {item.label_colors}")
                    return
        raise ValueError(f"Item with ID {item_id} not found")