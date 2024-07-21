import json
from util.replicate import runRequests
from util.parse import parseTimetable
from util.logging import Logger

class EdupageScraper:
    def __init__(self):
        self.logger = Logger("EdupageScraper")

    def scrapeTimetable(self):
        with self.logger.timer("Fetching data"):
            data = runRequests()

        with self.logger.timer("Parsing data"):
            timetable = parseTimetable(data)

        return timetable

    def run(self):
        logger = Logger("main")

        try:
            timetable = self.scrapeTimetable()
        except Exception as e:
            logger.warning(f"An error occurred: {e}")
            logger.info("Running selenium scraper to refetch requests")
            from util.selenium import SeleniumScraper
            s = SeleniumScraper(logger)
            s.scrapeRequestsToFile()
            try:
                timetable = self.scrapeTimetable()            
            except Exception as e:
                logger.error(f"FATAL: Failed even after selenium rerun, something is wrong!\n{e}")
                exit()

        with open("timetable.json", 'w', encoding="utf-8") as f:
            f.write(json.dumps(timetable, indent=4))

if __name__ == "__main__":
    s = EdupageScraper()
    s.run()