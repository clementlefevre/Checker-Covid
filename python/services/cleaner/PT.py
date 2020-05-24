import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

    filename = "total_url_esri_1.csv"
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df, covid, option="url_1")

    df_translated["date"] = pd.to_datetime(df_translated["date"], unit="ms")
    df_translated["date"] = df_translated["date"].dt.date

    df_melted_url_1 = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted_url_1["source_url"] = covid.params["url_esri_1"]
    df_melted_url_1["filename"] = filename

    filename = "total_url_esri_2.csv"
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df, covid, option="url_2")

    df_translated["date"] = pd.to_datetime(df_translated["date"], unit="ms")
    df_translated["date"] = df_translated["date"].dt.date

    df_melted_url_2 = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted_url_2["source_url"] = covid.params["url_esri_1"]
    df_melted_url_2["filename"] = filename

    df_melted = pd.concat([df_melted_url_1, df_melted_url_2], axis=0)
    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)

    df_melted["country"] = covid.country

    return df_melted
