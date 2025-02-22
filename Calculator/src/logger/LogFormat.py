import logging
import coloredlogs

class LogFormat:

    def __init__(self, name):
        self.logger = self.setup_logger(name)
    
    def setup_logger(self,name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler("Calculator/logs/error.log")
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
        
        custom_level_styles = {
            'info': {'color': 'blue'},
            'warning': {'color': 'yellow', 'bold': True},
            'error': {'color': 'red'},
            'critical': {'color': 'red', 'bold': True}
        }
        
        coloredlogs.install(level='INFO', logger=logger, fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level_styles=custom_level_styles)

        return logger
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
        
    def critical(self, message):
        self.logger.critical(message)