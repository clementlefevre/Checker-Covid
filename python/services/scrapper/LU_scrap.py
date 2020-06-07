import pandas as pd


def download(covid):

    df = pd.read_html(covid.params["url"])
    df_tested = df[2]
    df_icu = df[10]

    df_tested.to_csv(f"{covid.path_to_save}/tested.csv", index=False)
    df_icu.to_csv(f"{covid.path_to_save}/icu.csv", index=False)
