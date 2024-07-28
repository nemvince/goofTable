import json
import logging

from scraper.log import LoggerFactory

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumScraper:
    def __init__(self):
        self.slogger = logging.getLogger("selenium")
        self.logger = LoggerFactory.create_logger("SeleniumScraper")
        self.logger.info("Creating a new instance of the Chrome driver")

        # Create capabilities
        options = webdriver.ChromeOptions()
        arguments = [
            "--headless",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-infobars",
            "--mute-audio",
            "--disable-popup-blocking",
            "--disable-web-security",
            "--ignore-certificate-errors",
            "--enable-logging",
        ]
        for arg in arguments:
            options.add_argument(arg)

        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        try:
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            self.logger.error(
                f"Failed to create a new instance of the Chrome driver: {e}"
            )
            exit()

    def scrapeRequestsToFile(self, url="https://petrik.edupage.org/timetable/"):
        self.driver.get(url)

        timeout = 10

        try:
            self.logger.info("Waiting for the page to load")
            element = ec.presence_of_element_located((By.CLASS_NAME, "print-sheet"))
            WebDriverWait(self.driver, timeout).until(element)
        except TimeoutException:
            self.logger.error("Timed out waiting for page to load")
            self.driver.quit()
            exit()

        logs = self.driver.get_log("performance")
        network_logs = [
            json.loads(log["message"])["message"]
            for log in logs
            if json.loads(log["message"])["message"]["method"]
            == "Network.requestWillBeSent"
        ]
        target_requests = [
            log for log in network_logs if "__func" in log["params"]["request"]["url"]
        ]

        self.driver.quit()

        if not target_requests:
            self.logger.error("No target requests found")
            exit()

        idx = 0
        for request in target_requests:
            filename = "ttv" if idx == 0 else "reg"
            idx += 1
            with open(f"req/{filename}.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(request, indent=4))
