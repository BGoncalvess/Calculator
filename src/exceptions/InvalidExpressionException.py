from src.formats.LogFormat import LogFormat


class InvalidExpressionException(Exception):

    def __init__(self, message, logger):
        super().__init__(message)
        self.message = message
        self.logger = logger

    def error(self):
        self.logger.error(self.message)
