import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def _clean_apify(covid):

    filename = "total.csv"

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

    df_melt["source_url"] = covid.params["url_apify"]
    df_melt["filename"] = filename
    df_melt["country"] = covid.country

    return df_melt


def _clean_sst(covid):
    filename = "current_sst.csv"

    df = pd.read_csv(f"{covid.path_to_save}/{filename}", encoding="utf-8")
    df = df[df["area"] == "Hele landet"]

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

    df_melt["source_url"] = covid.params["url_sst_dk"]
    df_melt["filename"] = filename
    df_melt["country"] = covid.country

    return df_melt


def clean(covid):

    df_melt_apify = _clean_apify(covid)

    df_melt_sst = _clean_sst(covid)

    return pd.concat([df_melt_apify, df_melt_sst], axis=0)
