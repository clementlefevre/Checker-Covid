
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid, scrap=True):

    if scrap:
        covid.scrapper()

    source_name = covid.params["url"]
    file_name = "AllgemeinDaten.csv"
    df = pd.read_csv(
        f"{covid.data_path}/raw/{covid.dt_created}/AllgemeinDaten.csv", sep=";"
    )

    df_translated = translate_and_select_cols(df, covid)
    df_translated["updated_on"] = pd.to_datetime(df_translated["updated_on"]).dt.date
    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date

    df_global = pd.melt(
        df_translated,
        id_vars=["updated_on", "date"],
        value_vars=["cases", "cum_tests", "curr_hospi", "curr_icu"],
        var_name="key",
        value_name="value",
    )

    df_global["source_url"] = source_name
    df_global["filename"] = file_name

    filename = "Epikurve.csv"
    df_cases = pd.read_csv(f"{covid.path_to_save}/{filename}", sep=";")
    df_cases = translate_and_select_cols(df_cases, covid)
    df_cases["updated_on"] = pd.to_datetime(df_cases["updated_on"]).dt.date
    df_cases["date"] = pd.to_datetime(df_cases["date"], format="%d.%m.%Y").dt.date

    df_cases_melted = pd.melt(
        df_cases,
        id_vars=["updated_on", "date"],
        value_vars=["new_cases"],
        var_name="key",
        value_name="value",
    )

    df_cases_melted["source_url"] = source_name
    df_cases_melted["filename"] = filename

    # Apify

    filename = "total.csv"
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df, covid, "_apify")

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

    df_melt.dropna(inplace=True)

    df_autria_all = pd.concat([df_global, df_cases_melted, df_melt], axis=0)

    df_autria_all = df_autria_all.drop_duplicates(["key", "date"], keep="last")

    df_autria_all["country"] = covid.country
    return df_autria_all

