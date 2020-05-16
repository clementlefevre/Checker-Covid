import warnings
import logging

warnings.simplefilter(action="ignore", category=FutureWarning)

from datetime import date
import pandas as pd

from services.s3_bucket import get_current_latest_file_on_s3, upload_to_s3


def update_current_s3d_dataset(df_new):
    """combine new and current dataset

    This avoid the datagap if the new dataset failed to scrap all countries

    :param df_new: the resulting data of the scrapping and cleangin operation
    :type df_new: pd.DataFrame
    """

    has_error = True

    df_new["updated_on"] = pd.to_datetime(df_new["updated_on"])

    df_current_s3 = get_current_latest_file_on_s3()

    if df_current_s3.shape[0] > 0:
        df_current_s3["updated_on"] = pd.to_datetime(df_current_s3["updated_on"])
        df_current_s3["date"] = pd.to_datetime(df_current_s3["date"]).dt.date

        # https://stackoverflow.com/a/35088066/3209276
        # df = df.loc[~df.index.duplicated(keep='first')]
        try:

            df_concat = pd.concat([df_current_s3, df_new], axis=0, ignore_index=True)
            df_updated = (
                df_concat.sort_values("updated_on")
                .groupby(["country", "date", "key"])
                .last()
                .reset_index()
            )
            has_error = False
        except:
            logging.exception("Failure while concatening current dataset with new one:")
    else:
        df_updated = df_new
        has_error = False

    df_updated = df_updated[[col for col in df_updated.columns if "Unnamed" not in col]]

    upload_to_s3(df_updated, df_new, has_error)
