import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import requests
import re
import pandas as pd
from zipfile import ZipFile
from io import BytesIO, StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

from pathlib import Path
import pygsheets
from tabula import read_pdf

from lxml import html


from datetime import datetime, timedelta


now = datetime.now()  # current date and time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


# do not understand the table
def download_estonia():
    gc = pygsheets.authorize(service_file="data/berlingeocoding-b8a4b359adfb.json")
    wks = gc.open_by_url(COUNTRIES["estonia"]["url"])
    wk = wks.worksheet_by_title("Data about Estonia")
    df = wk.get_as_df()
    df.to_excel("data/estonia/covid19_in_Estonia_Public_Data about Estonia.xlsx")


# could not find anything
def download_finland():
    URL = "http://sampo.thl.fi/pivot/prod/en/epirapo/covid19case/fact_epirapo_covid19case.json"

    response = requests.get(URL, headers=headers)
    return response
    return pd.DataFrame_fro(response.json())


# ?? what do we need ?
def download_netherland():
    # https://www.stichting-nice.nl/
    response_global = requests.get(COUNTRIES["netherland"]["url_global"])
    df_global = pd.DataFrame([response_global.json()])
    df_global["date"] = date = now.strftime("%Y-%m-%d")

    df_new_intake = pd.read_json(COUNTRIES["netherland"]["url_new_intake"])
    df_intake_count = pd.read_json(COUNTRIES["netherland"]["url_intake_count"])
    df_icu = pd.read_json(COUNTRIES["netherland"]["url_icu"])
    df_ic_count = pd.read_json(COUNTRIES["netherland"]["url_ic_count"])

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    pageContent = requests.get(COUNTRIES["netherland"]["url_actuel"], headers=headers)
    tree = html.fromstring(pageContent.content)
    table = tree.xpath("//table[@class='table table-responsive']//span")
    tested_persons = table[0].text_content()

    return (df_global, df_new_intake, df_intake_count, df_icu, df_ic_count)


def download_norway():

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    pageContent = requests.get(COUNTRIES["norway"]["url_case"], headers=headers)
    tree = html.fromstring(pageContent.content)

    cases_string = tree.xpath("//li[contains(.,'people with confirmed COVID-19')]")[
        0
    ].text_content()
    tests_string = tree.xpath("//li[contains(.,'have been tested for coronavirus')]")[
        0
    ].text_content()

    pattern_cases = "Total of(.*?)people with confirmed COVID-19"

    substring = re.search(pattern_cases, cases_string).group(1)
    total_cases = int(substring.replace(" ", ""))

    pattern_tests = "A total of(.*?)have been tested for coronavirus"

    substring = re.search(pattern_tests, tests_string).group(1)
    total_tested = int(substring.replace(" ", ""))

    return {"total_cases": total_cases, "total_tested": total_tested}

