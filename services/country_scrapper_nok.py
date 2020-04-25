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


def download_spain():
    response_values = requests.get(COUNTRIES["spain"]["url_start"], headers=headers)
    tree = html.fromstring(response_values.content)
    pdf_url = tree.xpath("//a[contains(.,'Actualización nº')]")
    filename = pdf_url[0].attrib["href"].split("/")[-1]
    full_path = (
        "https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/"
        + filename
    )
    all_tables = read_pdf(full_path, guess=True, multiple_tables=True, pages="all")

    df_1 = all_tables[0]
    df_1_geo = df_1.iloc[:, 0]
    df_cases = df_1["Confirmados COVID-19"].str.split(" ", expand=True)
    df_cases.columns = ["cases_total", "cases_new"]

    df_tests = df_1["Confirmados COVID-19.1"].str.split(" ", expand=True)
    df_tests.drop(2, inplace=True, axis=1)
    df_tests.columns = ["test_total", "test_new"]

    df_cases_test = pd.concat([df_1_geo, df_cases, df_tests], axis=1)
    df_cases_test.rename(columns={df_cases_test.columns[0]: "geo"}, inplace=True)
    df_cases_test = df_cases_test[df_cases_test["geo"] == "ESPAÑA"]

    df_2 = all_tables[1]
    df_2_geo = df_2.iloc[:, 0]
    df_2_geo = pd.DataFrame({"geo": df_2_geo})
    df_2_hospi = (
        df_2.iloc[:, 1]
        .str.replace("¥ ", "")
        .str.replace("¥", "")
        .str.replace(".", "")
        .str.split(" ", expand=True)
    )
    df_2_hospi.columns = ["hospi_total", "hospi_new", "uci_total"]

    df_3_uci_new = pd.DataFrame({"uci_new": df_2.iloc[:, 2]})

    df_2_clean = pd.concat([df_2_geo, df_2_hospi, df_3_uci_new], axis=1)

    # find Andalucia to start the table :
    index_andalucia = df_2_clean.index[df_2_clean["geo"] == "Andalucía"].tolist()[0]
    df_2_clean = df_2_clean[df_2_clean.index >= index_andalucia]

    cols = ["hospi_total", "hospi_new", "uci_total", "uci_new"]
    df_2_clean = df_2_clean[cols].fillna(0)  # .apply(lambda x: x.astype(int))
    for col in cols:
        df_2_clean[col] = df_2_clean[col].str.extract("(\d+)").astype(float)

    df_hospi_icu = pd.DataFrame(df_2_clean[cols].sum()).T
    df_hospi_icu["geo"] = "ESPAÑA"
    df_all = pd.concat(
        [df_cases_test.reset_index(), df_hospi_icu.reset_index()], axis=1
    )

    return df_all

