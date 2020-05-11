import sys

import os


from config import COUNTRIES, HEADERS

from datetime import datetime

from pathlib import Path


from services.country_scrappers import *

import logging

logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.ERROR)


file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "data"))


def create_folder():
    for country in COUNTRIES.keys():
        Path(f"{file_path}/countries/{country}").mkdir(parents=True, exist_ok=True)


class COVID:
    def __init__(
        self,
        country,
        update=True,
        dt_created=datetime.now(),  # .strftime("%Y-%m-%d"),
        data={},
    ):
        self.country = country
        self.update = update
        self.dt_created = dt_created
        self.dt_created_date_str = self.dt_created.strftime("%Y-%m-%d")
        self.data = {}
        self.params = COUNTRIES[country]
        self.countries_list = COUNTRIES.keys()

        self.data_path = f"{file_path}/countries/{country}"
        self.HEADERS = HEADERS
        create_folder()
        self.path_to_save = f"{self.data_path}/raw/{self.dt_created_date_str}"
        Path(self.path_to_save).mkdir(parents=True, exist_ok=True)

    def scrapper(self):
        return self.params["scrapper"](self)

    def cleaner(self):
        if self.update:
            self.scrapper()

        return self.params["cleaner"](self)
