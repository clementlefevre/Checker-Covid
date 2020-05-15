import pandas as pd
import requests
from datetime import datetime, date
from lxml import html
import js2xml
from urllib import parse
import time


def get_provinces_links(covid):

    r = requests.get(covid.params["url_uclm"])

    page_content = html.fromstring(r.content)
    provinces_links = page_content.xpath(
        '//div[@id="myDropdown"]//a[@class="dropdown-item"]/@href'
    )
    return provinces_links


def get_province_data(covid, province_link):
    r_province = requests.get(covid.params["url_uclm"] + province_link)
    doc = html.fromstring(r_province.content)
    script = doc.xpath(".//script")
    js_content = doc.xpath("//script//text()")

    parsed = js2xml.parse(js_content[7])
    date_data = parsed.xpath('//property[@name="data"]//arguments/string')
    dates = [st.text for st in date_data]
    df_dates = pd.DataFrame({"date": dates})
    df_dates["date"] = pd.to_datetime(df_dates["date"]).dt.date
    df_dates = df_dates[df_dates["date"] <= date.today()]

    value_path = parsed.xpath(
        '//*[property[identifier[@name="hospitalized"]]]/ancestor::array'
    )[0]
    value_path
    d = js2xml.make_dict(value_path)
    df = pd.DataFrame(d)

    s = (
        df.apply(lambda x: pd.Series(x["data"]), axis=1)
        .stack()
        .reset_index(level=1, drop=True)
    )
    s.name = "data"
    df2 = df.drop("data", axis=1).join(s)
    df2["data"] = pd.Series(df2["data"], dtype=object)
    df2 = df2[["label", "data"]]
    labels_to_filter = [
        "Total cases",
        "Active cases",
        "Hospitalized",
        "Critical (ICU)",
        "Total Recoveries",
        "Total Deaths",
    ]
    df2 = df2[df2["label"].isin(labels_to_filter)]

    df_all = pd.DataFrame()

    for label in labels_to_filter:
        df_label = df2[df2["label"] == label].reset_index()
        df_label = df_label[["label", "data"]]
        df_label[label] = df_label["data"]

        df_all = pd.concat([df_all, df_label[[label]]], axis=1)
    df_with_date = pd.concat([df_all, df_dates], axis=1)
    df_with_date.rename({"data": "value"})
    df_with_date["province"] = province_link.replace("?ccaa=", "")
    return df_with_date


def download(covid):
    df = pd.DataFrame()

    provinces_links = get_provinces_links(covid)

    for p in provinces_links:
        df_province = get_province_data(covid, p)
        df = pd.concat([df, df_province], axis=0)
        # time.sleep(3)

    df.to_csv(f"{covid.path_to_save}/total_uclm.csv", index=False)
