import logging
import os

from app.utils.loggers.log_destination import LogDestination


class FileLogDestination(LogDestination):
    def __init__(self, file_path: str):
        self.logger = logging.getLogger("FileLogger")
        self.logger.setLevel(logging.DEBUG)

        # Ensure the log directory exists
        log_dir = os.path.dirname(file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(file_path)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs):
        """Log an info level message."""
        self.logger.info(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        """Log an error level message."""
        self.logger.error(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """Log a warning level message."""
        self.logger.warning(message, extra=kwargs)

    def debug(self, message: str, **kwargs):
        """Log a debug level message."""
        self.logger.debug(message, extra=kwargs)

    def critical(self, message: str, **kwargs):
        """Log a critical level message."""
        self.logger.critical(message, extra=kwargs)

    def exception(self, message: str, **kwargs):
        """Log an exception level message."""
        self.logger.exception(message, extra=kwargs)
