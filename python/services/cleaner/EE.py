import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
from datetime import date, timedelta

from ..translator import translate_and_select_cols


def clean(covid):

    filename = "total.csv"

    df = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df = df.iloc[:, range(3, df.shape[1])]
    df_T = df.T
    df_T.columns = df_T.iloc[0]
    df_T = df_T.drop(df_T.index[0]).reset_index()
    df_T = df_T.rename(columns={"index": "date_original"})
    df_T["increment"] = df_T.index

    def set_date(row):
        return date(2020, 2, 5) + timedelta(days=row["increment"])

    df_T["date"] = df_T.apply(set_date, axis=1)
    df_translated = translate_and_select_cols(df_T, covid)

    df_translated.date = pd.to_datetime(df_translated.date).dt.date

    df_melt = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melt["updated_on"] = pd.to_datetime(covid.dt_created)

    df_melt["source_url"] = covid.params["url_spreadsheet"]
    df_melt["filename"] = filename
    df_melt["country"] = covid.country

    return df_melt
