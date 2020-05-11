import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

    filename = "total_cases_hospi_icu.csv"
    df = pd.read_csv(f"{covid.path_to_save}/{filename}")
    df_translated = translate_and_select_cols(df, covid)

    df_translated["date"] = pd.to_datetime(df["Date"], unit="ms").dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=["cases", "curr_hospi", "curr_icu"],
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = (
        covid.params["url_1"]
        + covid.dt_created.strftime("%Y-%m-%d")
        + covid.params["url_2"]
    )
    df_melted["updated_on"] = pd.to_datetime(covid.dt_created)

    df_melted["filename"] = filename
    df_melted["country"] = covid.country

    return df_melted
