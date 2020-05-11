import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean_aggregados(covid):

    filename = "total.csv"
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df = df[~df["FECHA"].isnull()]
    df["FECHA"] = pd.to_datetime(df.FECHA, format="%d/%m/%Y")

    groupy = df.groupby("FECHA").sum()

    groupy["cum_PCR+"] = groupy["PCR+"].diff()

    df_translated = translate_and_select_cols(groupy.reset_index(), covid)

    df_translated["date"] = df_translated["date"].dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = covid.params["url"]
    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)

    df_melted["filename"] = filename
    df_melted["country"] = covid.country

    return df_melted


def clean(covid):

    filename = "total_uclm.csv"
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df = df[~df["Hospitalized"].isnull()]
    df["date"] = pd.to_datetime(df.date, format="%Y-%m-%d")

    groupy = df.groupby("date").sum().reset_index()

    df_translated = translate_and_select_cols(groupy, covid, option="uclm")

    df_translated.date = pd.to_datetime(df_translated.date).dt.date

    df_melt = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melt["updated_on"] = pd.to_datetime(covid.dt_created)

    df_melt["source_url"] = covid.params["url_uclm"]
    df_melt["filename"] = filename
    df_melt["country"] = covid.country

    return df_melt
