from abc import ABC, abstractmethod

class LogDestination(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs):
        """Log an info level message."""
        pass

    @abstractmethod
    def error(self, message: str, **kwargs):
        """Log an error level message."""
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs):
        """Log a warning level message."""
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs):
        """Log a debug level message."""
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs):
        """Log a critical level message."""
        pass

    @abstractmethod
    def exception(self, message: str, **kwargs):
        """Log an exception level message."""
        pass
