import json

import requests

from scraper.config import config
from scraper.log import LoggerFactory


class Replicator:
    def __init__(self) -> None:
        self.logger = LoggerFactory.create_logger("Replicator")

    def replicate(self, request):
        url = request["params"]["request"]["url"]
        method = request["params"]["request"]["method"]
        headers = request["params"]["request"]["headers"]
        payload = request["params"]["request"]["postData"]

        if method == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, data=payload)

        self.logger.debug(f"Replicated request: {response.status_code}")

        return json.loads(response.text)

    def runRequests(self):
        with open(config.get_data_path("ttv.json"), "r", encoding="utf-8") as f:
            ttv_data = json.load(f)

        with open(config.get_data_path("reg.json"), "r", encoding="utf-8") as f:
            ttn_data = json.load(f)

        # get list of timetables
        ttv = self.replicate(ttv_data)

        # replace the placeholder with the latest timetable number
        ttn_data["params"]["request"]["postData"] = ttn_data["params"]["request"][
            "postData"
        ].replace("TTNUM_REPLACEME", ttv["r"]["regular"]["timetables"][-1]["tt_num"])

        # get the latest timetable
        reg = self.replicate(ttn_data)

        return reg
