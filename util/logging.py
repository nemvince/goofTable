from contextlib import contextmanager
import logging
import time
import colorlog

class Logger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a console handler
        handler = colorlog.StreamHandler()

        handler.setFormatter(colorlog.ColoredFormatter('%(asctime)s - %(log_color)s%(name)s:%(levelname)s: %(message)s'))

        self.logger.addHandler(handler)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    @contextmanager
    def timer(self, msg):
        start_time = time.time()
        yield
        end_time = time.time()
        self.info(f"{msg} took {round((end_time - start_time), 3)} seconds")
