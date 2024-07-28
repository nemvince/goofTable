import json

from scraper.config import config
from scraper.db import Database
from scraper.log import LoggerFactory, LoggerUtils
from scraper.parse import parseTimetable
from scraper.request import Replicator
from scraper.request import SeleniumScraper


class EdupageScraper:
    def __init__(self):
        self.logger = LoggerFactory.create_logger("EdupageScraper")
        self.replicator = Replicator()
        self.db = Database(config.get_db_url())

    def scrapeTimetable(self):
        with LoggerUtils.timer(self.logger, "Fetching data"):
            data = self.replicator.runRequests()

        if config.get("scraper.debug"):
            self.logger.debug("Writing data to file")
            with open(config.get_data_path("data.json"), "w") as f:
                json.dump(data, f)

        with LoggerUtils.timer(self.logger, "Parsing data"):
            timetable = parseTimetable(data)

        return timetable

    def run(self):
        try:
            timetable = self.scrapeTimetable()
        except Exception as e:
            self.logger.warning(f"An error occurred: {e}")
            self.logger.info("Running selenium scraper to refetch requests")
            s = SeleniumScraper()
            with LoggerUtils.timer(self.logger, "Scraping requests"):
                s.scrapeRequestsToFile()
            try:
                timetable = self.scrapeTimetable()
            except Exception as e:
                self.logger.error(
                    f"FATAL: Failed even after selenium rerun, something is wrong!\n{e}"
                )
                exit()

        self.logger.info("Successfully scraped timetable data")

        with LoggerUtils.timer(self.logger, "Inserting data into database"):
            self.db.update_timetable(timetable)
