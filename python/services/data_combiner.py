import warnings
import logging

import pandas as pd

from services.s3_bucket import get_current_latest_file_on_s3, upload_to_s3

warnings.simplefilter(action="ignore", category=FutureWarning)

cols_of_scope = [
    "country",
    "date",
    "key",
    "updated_on",
    "value",
    "source_url",
    "filename",
]


def filter_on_latest_update(df):
    """we drop the duplicates after having converted the data to datetime and the
    updated_on to pd.Timestamp

    :param df: [description]
    :type df: [type]
    :return: [description]
    :rtype: [type]
    """

    df["updated_on"] = df["updated_on"].apply(pd.Timestamp)

    df["date"] = pd.to_datetime(df["date"]).dt.date

    df_clean = (
        df.sort_values("updated_on").groupby(["country", "date", "key"]).tail(1)
    )

    return df_clean[cols_of_scope]


def update_current_s3d_dataset(df_new):
    """combine new and current dataset

    This avoid the datagap if the new dataset failed to scrap all countries

    :param df_new: the resulting data of the scrapping and cleangin operation
    :type df_new: pd.DataFrame
    """

    has_error = True

    df_new_clean = filter_on_latest_update(df_new)
    df_current_s3 = get_current_latest_file_on_s3()

    if df_current_s3.shape[0] > 0:

        # https://stackoverflow.com/a/35088066/3209276
        # df = df.loc[~df.index.duplicated(keep='first')]
        try:
            df_current_s3_clean = filter_on_latest_update(df_current_s3)

            df_concat = pd.concat(
                [df_current_s3_clean, df_new_clean], axis=0, ignore_index=True
            )
            df_updated = filter_on_latest_update(df_concat)

            has_error = False
        except Exception:

            logging.exception(
                "Failure while concatening current dataset with new one:"
            )
    else:

        df_updated = df_new_clean
        has_error = False

    # df_updated = df_updated[cols_of_scope]
    logging.info(
        f"\n{df_updated.updated_on.value_counts().sort_values(ascending=False).head()}"
    )
    upload_to_s3(df_updated, df_new_clean, has_error)
