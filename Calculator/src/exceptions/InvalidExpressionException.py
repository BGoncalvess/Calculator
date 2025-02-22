from logger.LogFormat import LogFormat

class InvalidExpressionException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def error(self):
        # Create a LogFormat instance and log the exception
        LogFormat().error(self.message)