from collections import deque
from formats.HistoryFormat import HistoryFormat

class HistoryStorage:
    def __init__(self, max_size=10):
        self.history = deque(maxlen=max_size)
        self.counter = 1

    def add_entry(self, expression, result):
        entry = HistoryFormat(self.counter, expression, result)
        self.history.append(entry)
        self.counter += 1

    def get_history(self):
        if self.history:
            return list(self.history)
        return None