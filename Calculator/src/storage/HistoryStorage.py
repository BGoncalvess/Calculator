from formats.HistoryFormat import HistoryFormat

class HistoryStorage:

    history = []
    counter = 1
    MAX_HISTORY_SIZE = 11

    @classmethod
    def add_history(cls, expression, result):
        history_expression_formatted = HistoryFormat(cls.counter, expression, result)
        cls.history.append(history_expression_formatted)
        cls.counter += 1

        if len(cls.history) > cls.MAX_HISTORY_SIZE:
            cls.history.pop(0)

    @classmethod
    def get_history(cls):
        return cls.history if cls.history else None