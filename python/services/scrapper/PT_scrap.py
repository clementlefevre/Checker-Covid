import pandas as pd
import requests

from services.country_scrappers import headers


def download_portugal(covid):

    # https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/
    r = requests.get(covid.params["url_esri_1"], headers=headers)
    df = pd.DataFrame(r.json()["features"])["attributes"].apply(pd.Series)

    df.to_csv(f"{covid.path_to_save}/total_url_esri_1.csv", index=False)

    r = requests.get(covid.params["url_esri_2"], headers=headers)
    df = pd.DataFrame(r.json()["features"])["attributes"].apply(pd.Series)

    df.to_csv(f"{covid.path_to_save}/total_url_esri_2.csv", index=False)
