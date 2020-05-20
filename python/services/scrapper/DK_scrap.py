import pandas as pd
from datetime import datetime
import re


def download_denmark(covid):
    df_apify = pd.read_json(covid.params["url_apify"])
    df_apify.to_csv(f"{covid.path_to_save}/total.csv")

    df_cases_sst = pd.read_html(
        covid.params["url_sst_dk"], match="Smittede", header=0,
    )[0]

    df_cases_sst["date"] = covid.dt_created_date_str
    df_cases_sst.columns = [c.strip() for c in df_cases_sst.columns]
    df_cases_sst.rename(columns={"Unnamed: 0": "area"}, inplace=True)

    df_cases_sst.to_csv(
        f"{covid.path_to_save}/total_cases_sst.csv",
        index=True,
        encoding="utf-8",
    )

    all_df = pd.read_html(
        covid.params["url_sst_dk"],
        match="Antal indlagte på sygehus i alt",
        header=0,
    )

    df_sst_dk = all_df[0]
    df_sst_dk["date"] = covid.dt_created_date_str
    df_sst_dk.columns = [c.strip() for c in df_sst_dk.columns]
    df_sst_dk.rename(columns={"Unnamed: 0": "area"}, inplace=True)

    df_sst_dk.to_csv(
        f"{covid.path_to_save}/current_sst.csv", index=True, encoding="utf-8"
    )

    # cum_hosp
    df_cum_hosp = pd.read_html(
        covid.params["url_sst_dk"],
        match="Bekræftede COVID-19 tilfælde i alt",
        header=0,
    )[0]

    # we rename the column to avoid spec characters :
    cols_names = [
        " ".join(re.findall(r"[a-zA-Z0-9]+", c)) for c in df_cum_hosp.columns
    ]
    df_cum_hosp.columns = cols_names

    df_cum_hosp["date"] = covid.dt_created_date_str

    df_cum_hosp.to_csv(
        f"{covid.path_to_save}/current_sst_hospi.csv",
        index=True,
        encoding="utf-8",
    )

    # cum_icu
    df_cum_icu = pd.read_html(
        covid.params["url_sst_dk"],
        match="Bekræftede COVID-19 tilfælde i alt",
        header=0,
    )[1]

    # we rename the column to avoid spec characters :
    cols_names = [
        " ".join(re.findall(r"[a-zA-Z0-9]+", c)) for c in df_cum_icu.columns
    ]
    df_cum_icu.columns = cols_names

    df_cum_icu["date"] = covid.dt_created_date_str
    df_cum_icu.to_csv(
        f"{covid.path_to_save}/current_sst_icu.csv",
        index=True,
        encoding="utf-8",
    )
