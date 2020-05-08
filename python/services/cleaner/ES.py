import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

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
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = covid.country

    return df_melted
