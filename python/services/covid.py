import sys

from config import COUNTRIES

from datetime import datetime

from pathlib import Path


from services.country_scrappers import *

import logging
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)



def create_folder():
    for country in COUNTRIES.keys():
        Path(f"../data/countries/{country}").mkdir(parents=True, exist_ok=True)


class COVID:
    def __init__(self, country, dt_created=now.strftime("%Y-%m-%d"), data={}):
        self.country = country
        self.dt_created = dt_created
        self.data = {}
        self.params = COUNTRIES[country]
        self.countries_list = COUNTRIES.keys()
        self.data_path = f"../data/countries/{country}"
        # self.COUNTRIES = COUNTRIES
        create_folder()
        self.path_to_save = f"{self.data_path}/raw/{self.dt_created}"
        Path(self.path_to_save).mkdir(parents=True, exist_ok=True)

    def scrapper(self):
        return self.params["scrapper"](self)

    def cleaner(self):

        return self.params["cleaner"](self)

