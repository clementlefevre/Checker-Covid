import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

    covid.scrapper()
    filename = "total.csv"

    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    groupy = df.groupby("data").sum().reset_index()
    df_translated = translate_and_select_cols(groupy, covid)

    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=[
            "curr_icu",
            "curr_hospi",
            "new_cases",
            "cases",
            "tested",
            "cum_tests",
        ],
        var_name="key",
        value_name="value",
    )

    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = covid.country
    df_melted["source_url"] = covid.params["url"]

    return df_melted
