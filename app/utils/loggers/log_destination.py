from abc import ABC, abstractmethod


class LogDestination(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs):
        """Log an info level message."""

    @abstractmethod
    def error(self, message: str, **kwargs):
        """Log an error level message."""

    @abstractmethod
    def warning(self, message: str, **kwargs):
        """Log a warning level message."""

    @abstractmethod
    def debug(self, message: str, **kwargs):
        """Log a debug level message."""

    @abstractmethod
    def critical(self, message: str, **kwargs):
        """Log a critical level message."""

    @abstractmethod
    def exception(self, message: str, **kwargs):
        """Log an exception level message."""
