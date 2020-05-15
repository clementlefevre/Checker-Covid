
import pandas as pd
import requests
from datetime import datetime, date

def download_netherland(covid):

    ## new cases
    r = requests.get(covid.params["url_new_intake"])
    df_1 = pd.DataFrame(pd.DataFrame(r.json()).iloc[0])[0].apply(pd.Series)
    df_1.columns = ["date", "new_cases"]
    df_2 = pd.DataFrame(pd.DataFrame(r.json()).iloc[1])[1].apply(pd.Series)
    df_2.columns = ["date", "new_suspected_cases"]

    ## new ICU
    r = requests.get(covid.params["url_intake_count"])
    df_curr_icu = pd.DataFrame(r.json())

    df_curr_icu.columns = ["date", "curr_icu"]

    # IC with at least one COVID case
    r = requests.get(covid.params["url_icu"])
    df_icu = pd.DataFrame(r.json())
    df_icu.columns = ["date", "icu_with_al_one_case"]

    # ICU Cumulative
    r = requests.get(covid.params["url_ic_cumulative"])
    df_icu_cum = pd.DataFrame(r.json())
    df_icu_cum.columns = ["date", "cum_icu"]

    df = pd.merge(df_1, df_2, on="date")
    df = pd.merge(df, df_curr_icu, on="date")
    df = pd.merge(df, df_icu, on="date")
    df = pd.merge(df, df_icu_cum, on="date")

    df.to_csv(f"{covid.path_to_save}/total.csv", index=False)

    # RIVM
    all_df = pd.read_html(covid.params["url_rivm"])

    df = all_df[0]
    df.T

    df[1] = df[1].str.extract("(\d*\.?\d+)").replace("\.", "", regex=True)
    df_T = df.T

    new_header = df_T.iloc[0]  # grab the first row for the header
    df_T = df_T[1:]  # take the data less the header row
    df_T.columns = new_header
    df_result = df_T.head(1)
    df_result["date"] = datetime.now().strftime("%Y-%m-%d")
    df_result.to_csv(f"{covid.path_to_save}/current_rivm.csv", index=False)

