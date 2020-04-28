import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):
    filename = "RKI.csv"

    covid.scrapper()
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    groupy = df.groupby("Meldedatum").sum()

    groupy_cum = groupy.cumsum()
    groupy_cum.columns = ["cum_" + c for c in groupy.columns]

    df_all = pd.concat([groupy, groupy_cum], axis=1).reset_index()

    df_translated = translate_and_select_cols(df_all, covid)
    df_translated["date"] = pd.to_datetime(df_translated["date"])
    df_translated["date"] = df_translated["date"].dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = covid.params["url_rki"]
    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = covid.country

    return df_melted

