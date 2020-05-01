import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from services.translator import translate_and_select_cols


def clean(covid):
    if covid.update:
        covid.scrapper()
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

    filename = "current_icu.csv"
    df_icu_current = pd.read_csv(f"{covid.path_to_save}/{filename}")
    df_icu_current.columns = ["key", "value_1", "value_2"]
    df_icu_current["value"] = (
        df_icu_current["value_1"].astype(str).str.replace(" ", "")
        + " "
        + df_icu_current["value_2"].fillna(" ").astype(str)
    )
    df_icu_current_t = df_icu_current.set_index("key")[["value"]].T
    df_icu_current_translated = translate_and_select_cols(df_icu_current_t, covid)

    icu_curr_updated_on = df_icu_current_translated.date.values[0]

    df_icu_current_translated["date"] = pd.to_datetime(
        df_icu_current_translated["date"]
    ).dt.date
    df_melt_icu_current = pd.melt(
        df_icu_current_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melt_icu_current["source_url"] = covid.params["url_current_icu"]
    df_melt_icu_current["filename"] = filename
    df_melt_icu_current["country"] = covid.country
    df_melt_icu_current["updated_on"] = icu_curr_updated_on

    df_melt_all = pd.concat([df_melt, df_melt_icu_current])
    return df_melt_all
