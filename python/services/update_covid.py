import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

from datetime import datetime
import pandas as pd
import boto3
import logging

urllib3_log = logging.getLogger("urllib3")
urllib3_log.setLevel(logging.CRITICAL)


import os

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "data"))

from config import COUNTRIES
from services.covid import COVID
from services import data_combiner


def update_all():

    ALL_EU = []

    for c in list(COUNTRIES.keys()):
        try:

            covid = COVID(c)
            logging.info(f"cleaning {c}...")
            ALL_EU.append(covid.cleaner())
            logging.info(f"{c}: cleaned.")
        except Exception as e:
            logging.error("Something went wrong...")
            logging.error(e)

    df_pop = pd.read_csv(f"{file_path}/tps00001_1_Data.csv", encoding="utf-8")
    df_pop = df_pop[df_pop["TIME"] == df_pop.TIME.max()][["TIME", "GEO", "Value"]]
    df_pop.columns = ["TIME", "alpha2", "pop_2019"]

    df = pd.DataFrame()
    for d in ALL_EU:
        df = pd.concat([df, d], axis=0)

    df = df[~df.value.isnull()]

    df = pd.merge(df, df_pop, left_on="country", right_on="alpha2")

    data_combiner.update_current_s3d_dataset(df)
