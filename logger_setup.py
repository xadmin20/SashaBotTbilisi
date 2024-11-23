# logger_setup.py

import sys
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
        # Не обрабатывать Ctrl+C
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.exception("Необработанное исключение", exc_info=(exc_type, exc_value, exc_traceback))

# Устанавливаем обработчик исключений
sys.excepthook = exception_handler
# Экспортируем настроенный логгер
__all__ = ["logger"]
