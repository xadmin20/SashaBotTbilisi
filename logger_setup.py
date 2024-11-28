# logger_setup.py

import sys

from django.conf import settings
from loguru import logger



# Удаляем стандартный обработчик, который Loguru добавляет по умолчанию
logger.remove()

# Формат для терминала
terminal_format = "<green>{time:HH:mm:ss}</green> | <level>{level} {file} {line} {function}</level> | <cyan>{message}</cyan>"

# Формат для файла
file_format = "{time} {level} {file} {line} {function} {message}"

# Обработчик для терминала
logger.add(
    sys.stdout,
    level="DEBUG",
    format=terminal_format,
)

# Обработчик для файла
logger.add(
    "logs/startbot.log",
    rotation="4 MB",
    level="INFO",
    format=file_format,
)

def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error(f"Необработанное исключение: {exc_type}, {exc_value}")
    logger.error(f"Трассировка: {exc_traceback}")

# Устанавливаем обработчик исключений
sys.excepthook = exception_handler
# Экспортируем настроенный логгер



class SendAdminNotification:
    """Send notification to admin"""

    def __init__(self, message):
        self.message = message

    def log(self, level, message):
        """Универсальный метод для логирования"""
        if settings.DEBUG:
            logger.debug(f"{message} (DEBUG mode): {self.message}")
        else:
            getattr(logger, level)(f"{message}: {self.message}")

    def error(self):
        self.log("error", "Admin notification error")
        return f"Error notification sent: {self.message}"

    def new_user(self):
        self.log("info", "New user notification")


__all__ = ["logger", "SendAdminNotification"]