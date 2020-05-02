import pandas as pd
import requests
from lxml import html


def download(covid):
    df_apify = pd.read_json(covid.params["url_apify"])
    df_apify.to_csv(f"{covid.path_to_save}/total_apify.csv", index=False)

    r = requests.get(covid.params["url_hospi_icu"], headers=covid.HEADERS)

    df_hospi_icu_html = pd.read_html(r.content)

    df_hospi_icu = df_hospi_icu_html[0]
    df_hospi_icu.columns = df_hospi_icu.iloc[0]

    df_hospi_icu.columns = ["area", "curr_hospi", "curr_ipc", "curr_icu", "dead"]

    date_update = get_update_date(r)

    df_hospi_icu["date"] = date_update

    df_hospi_icu.to_csv(f"{covid.path_to_save}/current_hospi_icu.csv", index=False)


def get_update_date(r):
    tree = html.fromstring(r.content)

    udpate_raw_string = tree.xpath("//strong[contains(.,'Updated on')]/text()")[0]

    from datetime import datetime
    import unicodedata

    update_string = unicodedata.normalize("NFKD", udpate_raw_string)
    update_string

    update_string = (
        update_string.replace("Updated on ", "").replace("at", "2020").replace(".", "")
    )
    print(update_string)
    datetime_update = datetime.strptime(update_string, "%d %B %Y %H:%M")
    return datetime_update
