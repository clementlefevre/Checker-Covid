import warnings
import pandas as pd
import logging
import os

from config import COUNTRIES
from services.covid import COVID
from services import data_combiner

warnings.simplefilter(action="ignore", category=FutureWarning)

urllib3_log = logging.getLogger("urllib3")
urllib3_log.setLevel(logging.CRITICAL)


file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..", "data")
)


def update_all(spec_countries=None):

    ALL_EU = []

    if spec_countries is not None:
        countries_to_update = spec_countries
    else:
        countries_to_update = list(COUNTRIES.keys())

    for c in countries_to_update:
        try:

            covid = COVID(c)
            logging.info(f"cleaning {c}...")
            ALL_EU.append(covid.cleaner())
            logging.info(f"{c}: cleaned.")
        except Exception as e:
            logging.exception(
                f"Something went wrong during the scraping of country : {c}"
            )
            logging.critical(e, exc_info=True)

    logging.info(f"merging data with TSP POP...")

    df = pd.DataFrame()
    for d in ALL_EU:
        df = pd.concat([df, d], axis=0)

    df = df[~df.value.isnull()]

    data_combiner.update_current_s3d_dataset(df)
