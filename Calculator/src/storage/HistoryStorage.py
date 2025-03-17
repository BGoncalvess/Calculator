import flet as ft
from formats.HistoryFormat import HistoryFormat

class HistoryStorage:

    history = []
    counter = 1
    MAX_HISTORY_SIZE = 11
    STORAGE_KEY = "calculator_history"

    @classmethod
    def initialize(cls, page: ft.Page):
        cls.page = page
        saved_history = cls.page.client_storage.get(cls.STORAGE_KEY)
        if saved_history:
            cls.history = [HistoryFormat(**entry) for entry in saved_history]
            cls.counter = max((entry.index for entry in cls.history), default=-1) + 1
        else:
            cls.history = []
            cls.counter = 1

    @classmethod
    def add_history(cls, expression, result):
        history_entry = HistoryFormat(cls.counter, expression, result)
        cls.history.append(history_entry)
        cls.counter += 1
        if len(cls.history) > cls.MAX_HISTORY_SIZE:
            cls.history.pop(0)
        cls._save_history()

    @classmethod
    def remove_history(cls, index):
        for i, entry in enumerate(cls.history):
            if entry.index == index:
                cls.history.pop(i)
                cls._save_history()
                break

    @classmethod
    def get_history(cls):
        return cls.history if cls.history else None

    @classmethod
    def _save_history(cls):
        serialized_history = [entry.to_dict() for entry in cls.history]
        cls.page.client_storage.set(cls.STORAGE_KEY, serialized_history)