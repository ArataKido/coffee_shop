from app.utils.loggers.log_destination import LogDestination
import logging
import colorlog


class ConsoleLogDestination(LogDestination):
    def __init__(self):
        self.logger = logging.getLogger("ConsoleLogger")
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()

        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
            datefmt=None,
            log_colors={
                "DEBUG": "green",
                "INFO": "blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

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
