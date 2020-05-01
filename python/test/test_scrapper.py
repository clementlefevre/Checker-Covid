

from config import COUNTRIES
from services.covid import COVID


def test_scrapper_SE():
    covid = COVID("SE",update=False)
    df = covid.cleaner()

    df
