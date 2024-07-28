import logging
import os
import sys

from scraper.log import LoggerFactory

import tomllib


class Config:
    def __init__(self):
        self.logger = LoggerFactory.create_logger("Config")

        conf_file = os.path.join(sys.path[0], "config.toml")

        try:
            with open(conf_file, "rb") as f:
                self.config = tomllib.load(f)
        except FileNotFoundError:
            self.logger.warn(
                f"Config file not found at {conf_file}, creating from example"
            )
            with open(conf_file, "wb") as f:
                with open(os.path.join(sys.path[0], "config.example.toml"), "rb") as ex:
                    f.write(ex.read())
                    self.config = tomllib.load(ex)
        finally:
            self.logger.setLevel(self.get_log_level())
            self.logger.info(f"Config loaded from {conf_file}")
            self.logger.debug(f"Config: {self.config}")

    def get(self, key):
        key_split = key.split(".")
        value = self.config
        try:
            for k in key_split:
                value = value[k]
            return value
        except KeyError:
            self.logger.error(f"Key {key} not found in config")
            return None

    def get_log_level(self):
        if self.get("scraper.debug"):
            return logging.DEBUG

        match self.get("scraper.loglevel"):
            case "debug":
                return logging.DEBUG
            case "info":
                return logging.INFO
            case "warn":
                return logging.WARN
            case "error":
                return logging.ERROR
            case "critical":
                return logging.CRITICAL
            case _:
                return logging.INFO

    def get_data_path(self, path):
        # check if the data directory exists, if not create it
        if not os.path.exists(os.path.join(sys.path[0], self.get("data.directory"))):
            os.makedirs(os.path.join(sys.path[0], self.get("data.directory")))

        return os.path.join(sys.path[0], self.get("data.directory"), path)

    def get_db_url(self):
        if self.get("db.type") == "sqlite":
            return f"sqlite:///{self.get_data_path(self.get('db.sqlite.name'))}"

        else:
            raise NotImplementedError(
                f"Database type {self.get('db.type')} not implemented"
            )
