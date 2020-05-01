from config import COUNTRIES
from services.covid import COVID


def test_scrapper_BE():
    covid = COVID("BE", update=False)
    df = covid.cleaner()


def test_BE_apify():
    covid = COVID("BE", update=True)
    df = covid.cleaner()

    df
