import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def _clean_country(covid):

    filename = "total.csv"

    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    groupy = df.groupby("data").sum().reset_index()
    df_translated = translate_and_select_cols(groupy, covid)

    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=[
            "curr_icu",
            "curr_hospi",
            "new_cases",
            "cases",
            "tested",
            "cum_tests",
        ],
        var_name="key",
        value_name="value",
    )

    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = covid.country
    df_melted["source_url"] = covid.params["url"]

    return df_melted


def _clean_regions(covid):

    filename = "total.csv"

    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    groupy = df.groupby(["data", "denominazione_regione"]).sum().reset_index()

    df_translated = translate_and_select_cols(groupy, covid)

    df_translated = df_translated[
        df_translated["region"].isin(["Emilia-Romagna", "Lombardia"])
    ]

    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date", "region"],
        value_vars=[
            "curr_icu",
            "curr_hospi",
            "new_cases",
            "cases",
            "tested",
            "cum_tests",
        ],
        var_name="key",
        value_name="value",
    )

    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = df_melted["region"]
    df_melted["source_url"] = covid.params["url"]

    return df_melted


def clean(covid):
    covid.scrapper()
    df_country = _clean_country(covid)
    df_regions = _clean_regions(covid)

    return pd.concat([df_country, df_regions], axis=0)
