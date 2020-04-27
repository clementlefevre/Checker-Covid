import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

    covid.scrapper()

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
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = covid.country

    return df_melted

    return df
