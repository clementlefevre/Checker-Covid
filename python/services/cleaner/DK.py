import warnings


import pandas as pd

from ..translator import translate_and_select_cols

warnings.simplefilter(action="ignore", category=FutureWarning)


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
    df_melt = df_melt[df_melt.key != "cases"]

    return df_melt


def _clean_sst_cases(covid):
    filename = "total_cases_sst.csv"

    df = pd.read_csv(
        f"{covid.path_to_save}/{filename}", encoding="utf-8", thousands="."
    )
    df = df[df["area"] == "Danmark"]

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


def _clean_sst(covid):
    filename = "current_sst.csv"

    df = pd.read_csv(
        f"{covid.path_to_save}/{filename}", encoding="utf-8", thousands="."
    )
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


def _clean_sst_hospi(covid):
    filename = "current_sst_hospi.csv"

    df = pd.read_csv(
        f"{covid.path_to_save}/{filename}", encoding="utf-8", thousands="."
    )

    df = df[df["Aldersgruppe"] == "I alt"][["Indlagte i alt", "date"]]
    df.columns = ["value", "date"]
    df["key"] = "cum_hospi"
    df["updated_on"] = pd.to_datetime(covid.dt_created)
    df["source_url"] = covid.params["url_sst_dk"]
    df["filename"] = filename
    df["country"] = covid.country

    return df


def _clean_sst_icu(covid):
    filename = "current_sst_icu.csv"

    df = pd.read_csv(
        f"{covid.path_to_save}/{filename}", encoding="utf-8", thousands="."
    )

    df = df[df["Alders gruppe"] == "I alt"][
        ["Indlagte p intensiv i alt", "date"]
    ]
    df.columns = ["value", "date"]
    df["key"] = "cum_icu"
    df["updated_on"] = pd.to_datetime(covid.dt_created)
    df["source_url"] = covid.params["url_sst_dk"]
    df["filename"] = filename
    df["country"] = covid.country

    return df


def clean(covid):
    df_melt_apify = _clean_apify(covid)
    df_melt_sst_cases = _clean_sst_cases(covid)
    df_melt_sst = _clean_sst(covid)
    df_sst_cum_hospi = _clean_sst_hospi(covid)
    df_sst_cum_icu = _clean_sst_icu(covid)

    return pd.concat(
        [
            df_melt_apify,
            df_melt_sst_cases,
            df_melt_sst,
            df_sst_cum_hospi,
            df_sst_cum_icu,
        ],
        axis=0,
    )
