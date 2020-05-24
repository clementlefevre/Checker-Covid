import warnings
import logging
import requests
import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime


logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(
    logging.ERROR
)

warnings.simplefilter(action="ignore", category=FutureWarning)

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
        ":HIGH:!DH:!aNULL"
    )
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def download_zip(file_url, target_path):
    """[download zip file and store it locally]

    [extended_summary]

    :param file_url: [description]
    :type file_url: [type]
    :param target_path: [description]
    :type target_path: [type]
    """

    url = requests.get(file_url, verify=False)
    zipfile = ZipFile(BytesIO(url.content))
    with zipfile as zip_ref:
        zip_ref.extractall(target_path)


def download_austria(covid):

    # from excel
    download_zip(covid.params["url"], covid.path_to_save)

    # Apify
    df = pd.read_json(covid.params["url_apify"])
    df.to_csv(f"{covid.path_to_save}/total.csv")


def download_belgium(covid):
    df = pd.read_json(covid.params["url_apify"])
    df.to_csv(f"{covid.path_to_save}/total_apify.csv", index=False)
    response = requests.get(covid.params["url"])

    with open(f"{covid.path_to_save}/COVID19BE.xlsx", "wb") as f:
        f.write(response.content)


def download_estonia(covid):
    csv_export_url = covid.params["url_spreadsheet"].replace(
        "/edit#gid=", "/export?format=csv&gid="
    )
    df = pd.read_csv(csv_export_url)
    df["date"] = datetime.now().strftime("%Y-%m-%d")
    df.to_csv(f"{covid.path_to_save}/total.csv")


# could not find total cases
def download_france_total(covid, url_values, field):

    url_values = url_values + datetime.now().strftime("%Y-%m-%d")

    response_values = requests.get(url_values, headers=headers)

    df = pd.DataFrame(
        response_values.json()["content"]["zonrefs"][0]["values"]
    )
    if field != "test":
        df = df[df.sexe == "0"]
    else:
        df = df[df.clage_covid == "0"].groupby("jour").sum().reset_index()

    if field == "hospitalized":
        df["cum_hospi"] = df["hosp"].cumsum()

    df.to_csv(f"{covid.path_to_save}/total_{field}.csv")


def download_france(covid):
    download_france_total(
        covid, covid.params["url_icu_values"], "icu",
    )
    download_france_total(
        covid, covid.params["url_hospitalized_values"], "hospitalized",
    )
    download_france_total(
        covid, covid.params["url_test_values"], "test",
    )


def download_germany(covid):
    df = pd.read_csv(covid.params["url_rki"])
    df.to_csv(f"{covid.path_to_save}/RKI.csv")


def download_ireland(covid):

    # https://geohive.maps.arcgis.com/apps/opsdashboard/index.html#/29dc1fec79164c179d18d8e53df82e96    date = now.strftime("%Y-%m-%d")
    i = 0
    url = (
        covid.params["url_1"]
        + covid.dt_created.strftime("%Y-%m-%d")
        + covid.params["url_2"]
    )

    r = requests.get(url, headers=headers)

    df = pd.DataFrame(r.json()["features"])["attributes"].apply(pd.Series)

    df.to_csv(f"{covid.path_to_save}/total_cases_hospi_icu.csv", index=False)


def download_italy(covid):

    df = pd.read_csv(covid.params["url"])
    df.to_csv(f"{covid.path_to_save}/total.csv", index=False)


def download_norway(covid):
    df = pd.read_json(covid.params["url_apify"])
    df.to_csv(f"{covid.path_to_save}/total.csv", index=False)


def download_switzerland(covid):
    df = pd.read_json(covid.params["url_apify"])
    df.to_csv(f"{covid.path_to_save}/total.csv", index=False)


def download_sweden(covid):
    df_apify = pd.read_json(covid.params["url_apify"])
    df_apify.to_csv(f"{covid.path_to_save}/total_apify.csv", index=False)

    df_icu = pd.read_html(covid.params["url_current_icu"])

    df_stats_icu = df_icu[0]
    df_stats_icu.to_csv(f"{covid.path_to_save}/current_icu.csv", index=False)


def download_owid(covid):
    df = pd.read_csv(covid.params["url"])
    df.to_csv(f"{covid.path_to_save}/total.csv", index=False)
