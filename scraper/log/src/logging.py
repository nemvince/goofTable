import logging
import time
from contextlib import contextmanager

import colorlog


class LoggerFactory:
    @staticmethod
    def create_logger(name, level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Create a console handler
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(asctime)s - %(log_color)s%(name)s:%(levelname)s: %(message)s"
            )
        )

        logger.addHandler(handler)

        return logger


class LoggerUtils:
    @contextmanager
    def timer(logger, msg):
        start_time = time.time()
        yield
        end_time = time.time()
        logger.info(f"{msg} took {round((end_time - start_time), 3)} seconds")
