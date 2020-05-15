import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

    filename = "total.csv"
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df_translated = df

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = covid.params["url_icu"]
    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)

    df_melted["filename"] = filename
    df_melted["country"] = covid.country

    filename_rivm = "current_rivm.csv"
    df_rivm = pd.read_csv(f"{covid.path_to_save}/{filename_rivm}")

    df_translated = translate_and_select_cols(df_rivm, covid)

    df_translated.date = pd.to_datetime(df_translated.date).dt.date

    df_melt_rivm = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melt_rivm["updated_on"] = pd.to_datetime(covid.dt_created)

    df_melt_rivm["source_url"] = covid.params["url_rivm"]
    df_melt_rivm["filename"] = filename
    df_melt_rivm["country"] = covid.country

    df = pd.concat([df_melted, df_melt_rivm], axis=0)

    df = df.drop_duplicates(["key", "date"], keep="last")

    return df

