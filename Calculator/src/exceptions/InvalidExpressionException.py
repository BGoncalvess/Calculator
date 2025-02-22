from logger.LogFormat import LogFormat

class InvalidExpressionException(Exception):
    def __init__(self, message, logger):
        super().__init__(message)
        self.message = message
        self.logger = logger

    def error(self):
        # Create a LogFormat instance and log the exception
        self.logger.error(self.message)