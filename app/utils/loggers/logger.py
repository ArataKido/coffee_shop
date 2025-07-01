import threading

from app.config import AppConfig
from app.utils.loggers.console_destination import ConsoleLogDestination
from app.utils.loggers.file_destination import FileLogDestination


# Inspired from Guru https://refactoring.guru/design-patterns/singleton/python/example#example-1
# and https://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example/
# Explanation: __call__ is called when the already-created (or scanned you can say) class is "called" to instantiate a new object.
# e.g. if you have a class A and you do A(), then __call__ is called.
# - On the other hand, __new__ should be implemented when you want to control the creation of a new object (class itself in our case),
# like when the class is being created or scanned for the first time, allocating memory for it, etc.
# - __init__ should be implemented when you want to control the initialization of the new object after it has been created.
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()  # Lock object to ensure thread safety

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self, app_config: AppConfig):
        self.destinations = []

        log_destinations = app_config.log_destinations.split(",")

        if "console" in log_destinations:
            self.destinations.append(ConsoleLogDestination())

        if "file" in log_destinations:
            self.destinations.append(FileLogDestination(app_config.log_file_path))

        self.initialized = True

    def info(self, message: str, **kwargs):
        for destination in self.destinations:
            destination.info(message, **kwargs)

    def error(self, message: str, **kwargs):
        for destination in self.destinations:
            destination.error(message, **kwargs)

    def warning(self, message: str, **kwargs):
        for destination in self.destinations:
            destination.warning(message, **kwargs)

    def debug(self, message: str, **kwargs):
        for destination in self.destinations:
            destination.debug(message, **kwargs)

    def critical(self, message: str, **kwargs):
        for destination in self.destinations:
            destination.critical(message, **kwargs)

    def exception(self, message: str, **kwargs):
        for destination in self.destinations:
            destination.exception(message, **kwargs)
