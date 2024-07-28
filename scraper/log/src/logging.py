import logging
import time
from contextlib import contextmanager

import colorlog


def get_log_level():
    try:
        from scraper.config import config

        return config.get_log_level()
    except ImportError:
        return logging.INFO


class LoggerFactory:
    @staticmethod
    def create_logger(name, level=None):
        if level is None:
            level = get_log_level()

        logger = logging.getLogger(name)

        # Create a console handler
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(asctime)s - %(log_color)s%(name)s:%(levelname)s: %(message)s"
            )
        )

        logger.addHandler(handler)
        logger.setLevel(level)

        return logger


class LoggerUtils:
    @contextmanager
    def timer(logger, msg):
        start_time = time.time()
        yield
        end_time = time.time()
        logger.info(f"{msg} took {round((end_time - start_time), 3)} seconds")
