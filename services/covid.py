import sys

from config import COUNTRIES

from datetime import datetime

from services.country_scrappers import *


def create_folder():
    for country in COUNTRIES.keys():
        Path(f"data/countries/{country}").mkdir(parents=True, exist_ok=True)


class COVID:
    def __init__(self, country, dt_created=now.strftime("%Y-%m-%d"), data={}):
        self.country = country
        self.dt_created = dt_created
        self.data = {}
        self.params = COUNTRIES[country]
        self.data_path = f"data/countries/{country}"
        create_folder()

    def scrapper(self):
        return self.params["scrapper"](self)

