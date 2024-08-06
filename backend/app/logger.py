import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')

    # Основной файл логов
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'app.log'),
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)

    # Файл для кэша логов
    cache_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'cache.log'),
        maxBytes=5*1024*1024,
        backupCount=3
    )
    cache_handler.setFormatter(formatter)
    cache_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(cache_handler)

    # Настройка уровней логирования для сторонних библиотек
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.INFO)

    return logger


def log_user_progress(user_id, progress):
    logger = logging.getLogger('user_progress')
    logger.info(f"User {user_id} progress: {progress}")
