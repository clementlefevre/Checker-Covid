import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd

import os


file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "data"))


df_lookup = pd.read_csv(f"{file_path}/lookup.csv", sep=",")


def translate_and_select_cols(df, covid, option=""):
    df_cols = pd.DataFrame(df.columns)
    df_cols.columns = ["original_field_name"]
    df_cols = pd.merge(
        df_cols,
        df_lookup[df_lookup["country"] == covid.country + option],
        on="original_field_name",
    )
    df_cols = df_cols[~df_cols["tub_name"].isnull()]
    cols_translations = df_cols.to_dict(orient="records")
    original_cols_to_filter = [d["original_field_name"] for d in cols_translations]
    tub_cols_to_filter = [d["tub_name"] for d in cols_translations]
    df = df[original_cols_to_filter]
    df.columns = tub_cols_to_filter

    return df
