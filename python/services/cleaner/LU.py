import warnings
import pandas as pd

from ..translator import translate_and_select_cols

warnings.simplefilter(action="ignore", category=FutureWarning)


def clean(covid):
    filename = "tested.csv"
    df_tested = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df_tested, covid)

    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date
    df_melt_tested = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    filename = "icu.csv"
    df_icu = pd.read_csv(f"{covid.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df_icu, covid)

    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date
    df_melt_icu = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df = pd.concat([df_melt_tested, df_melt_icu], axis=0)

    return df
