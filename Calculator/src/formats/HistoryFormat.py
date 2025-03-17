from datetime import datetime

class HistoryFormat:
    def __init__(self, index, expression, result, date=None):
        self.index = index
        self.date = date if date else str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.expression = expression
        self.result = result

    def to_dict(self):
        return {
            "index": self.index,
            "date": self.date,
            "expression": self.expression,
            "result": self.result
        }