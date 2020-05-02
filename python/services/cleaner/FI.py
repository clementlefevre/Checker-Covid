import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def _clean_apify(covid):

    filename = "total_apify.csv"

    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df, covid)

    df_translated.date = pd.to_datetime(df_translated.date).dt.date

    df_melt = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melt["updated_on"] = pd.to_datetime(covid.dt_created)
    df_melt["updated_on"] = df_melt["updated_on"].dt.date
    df_melt["source_url"] = covid.params["url_apify"]
    df_melt["filename"] = filename
    df_melt["country"] = covid.country

    df_melt = df_melt.drop_duplicates(["key", "date"], keep="last")

    return df_melt


def _clean_hospi_icu(covid):
    filename = "current_hospi_icu.csv"

    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df = df.tail(1)

    df_melt = pd.melt(
        df,
        id_vars=["date"],
        value_vars=df.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melt["updated_on"] = df_melt["date"]
    df_melt["date"] = pd.to_datetime(df_melt["date"]).dt.date
    df_melt["checked_on"] = pd.to_datetime(covid.dt_created)
    df_melt["checked_on"] = df_melt["checked_on"].dt.date
    df_melt["source_url"] = covid.params["url_hospi_icu"]
    df_melt["filename"] = filename
    df_melt["country"] = covid.country

    df_melt = df_melt.drop_duplicates(["key", "date"], keep="last")

    return df_melt


def clean(covid):
    covid.scrapper()
    df_melt_apify = _clean_apify(covid)
    df_melt_hospi_icu = _clean_hospi_icu(covid)

    return pd.concat([df_melt_apify, df_melt_hospi_icu], axis=0)
