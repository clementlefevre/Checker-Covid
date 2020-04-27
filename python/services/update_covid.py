import pandas as pd
import boto3
import logging

from config import COUNTRIES
from services.covid import COVID


def update_all():

    ALL_EU = []

    for c in COUNTRIES.keys():
        try:

            covid = COVID(c)
            logging.info(f"cleaning {c}")
            ALL_EU.append(covid.cleaner())
        except Exception as e:
            logging.error("Something went wrong...")
            logging.error(e)

    df_pop = pd.read_csv("../data/tps00001_1_Data.csv", encoding="utf-8")
    df_pop = df_pop[df_pop["TIME"] == df_pop.TIME.max()][["TIME", "GEO", "Value"]]
    df_pop.columns = ["TIME", "alpha2", "pop_2019"]

    df = pd.DataFrame()
    for d in ALL_EU:
        df = pd.concat([df, d], axis=0)

    df = df[~df.value.isnull()]

    df = pd.merge(df, df_pop, left_on="country", right_on="alpha2")

    df.to_csv("all_EU.csv", index=False)

    # Let's use Amazon S3
    s3 = boto3.resource("s3")

    # Upload a new file
    data = open("all_EU.csv", "rb")
    s3.Bucket("checkercovid").put_object(Key="all_EU.csv", Body=data)

