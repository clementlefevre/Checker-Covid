import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

    covid.scrapper()

    filename_hosp = "total_hospitalized.csv"
    df_hosp = pd.read_csv(f"{covid.data_path}/raw/{covid.dt_created}/{filename_hosp}")
    df_hosp_translated = translate_and_select_cols(df_hosp, covid)
    df_hosp_translated = df_hosp_translated[df_hosp_translated["sex"] == 0]
    df_hosp_melted = pd.melt(
        df_hosp_translated,
        id_vars=["date"],
        value_vars=["curr_hospi"],
        var_name="key",
        value_name="value",
    )

    df_hosp_melted["source_url"] = covid.params["url_hospitalized_values"]
    df_hosp_melted["filename"] = filename_hosp

    filename_icu = "total_icu.csv"
    df_icu = pd.read_csv(f"{covid.data_path}/raw/{covid.dt_created}/{filename_icu}")
    df_icu_tranlated = translate_and_select_cols(df_icu, covid)
    df_icu_tranlated = df_icu_tranlated[df_icu_tranlated["sex"] == 0]

    df_icu_melted = pd.melt(
        df_icu_tranlated,
        id_vars=["date"],
        value_vars=["curr_icu"],
        var_name="key",
        value_name="value",
    )

    df_icu_melted["source_url"] = covid.params["url_icu_values"]
    df_icu_melted["filename"] = filename_icu
    df_icu_melted

    filename_tests = "total_test.csv"
    df_test = pd.read_csv(f"{covid.data_path}/raw/{covid.dt_created}/{filename_tests}")
    df_test_translated = translate_and_select_cols(df_test, covid)

    df_test_melted = pd.melt(
        df_test_translated,
        id_vars=["date"],
        value_vars=["tested"],
        var_name="key",
        value_name="value",
    )

    df_test_melted["source_url"] = covid.params["url_test_values"]
    df_test_melted["filename"] = filename_tests

    df_france = pd.concat([df_hosp_melted, df_icu_melted, df_test_melted], axis=0)
    df_france["updated_on"] = pd.to_datetime(covid.dt_created)
    df_france["updated_on"] = df_france["updated_on"].dt.date
    df_france["country"] = covid.country
    return df_france

