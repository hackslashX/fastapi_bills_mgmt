import logging
import os
from logging.handlers import TimedRotatingFileHandler

from instance.config import config


class Logger:
    @staticmethod
    def get_logger(filename: str = "", name: str = ""):
        # Get directory
        parent_directory = os.path.dirname(filename)
        parent_directory = os.path.join(config.LOGS_DIR, parent_directory)

        # Create directory if not exists
        if parent_directory and not os.path.exists(parent_directory):
            os.makedirs(parent_directory)

        log_file_name = os.path.join(
            parent_directory, os.path.basename(filename) + ".log"
        )
        logging_level = config.LOGGING_LEVEL
        formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
        logger = logging.getLogger(name)

        # Add Time Rotating File Handler
        handler = TimedRotatingFileHandler(
            filename=log_file_name, when="midnight", interval=1, backupCount=30
        )
        handler.suffix = "%Y-%m-%d"
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging_level)

        # Also add stream handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger
