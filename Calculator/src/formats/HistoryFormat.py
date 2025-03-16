from datetime import datetime

class HistoryFormat:
    def __init__(self, index, expression, result):
        self.index = index
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.expression = expression
        self.result = result