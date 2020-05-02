import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


import pandas as pd

from services.s3_bucket import get_current_latest_file_on_s3, upload_to_s3


def update_current_s3d_dataset(df_new):

    df_current_s3 = get_current_latest_file_on_s3()
    df_concat = pd.concat([df_current_s3, df_new], axis=0, ignore_index=True)
    df_updated = df_concat.groupby(["country", "date", "key"]).last().reset_index()

    upload_to_s3(df_updated, df_new)
