from config import COUNTRIES
from services.covid import COVID


def test_scrapper_AT():
    covid = COVID("AT", update=False)
    df = covid.cleaner()
    df


def test_scrapper_BE():
    covid = COVID("BE", update=False)
    df = covid.cleaner()


def test_BE_():
    covid = COVID("BE", update=True)
    df = covid.cleaner()

    df


def test_IT_regions():
    covid = COVID("IT")
    df = covid.cleaner()
    df


def test_DK():
    covid = COVID("DK")
    df = covid.cleaner()
    df


def test_EE():
    covid = COVID("EE")
    df = covid.cleaner()
    df


def test_FI():
    covid = COVID("FI")
    df = covid.cleaner()
    df


def test_NL():
    covid = COVID("NL")
    df = covid.cleaner()
    df
