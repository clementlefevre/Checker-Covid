import os
from pathlib import Path

from datetime import datetime
import pandas as pd
from collections import namedtuple
import boto3
import logging
import pathlib

file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..", "data")
)


Path(f"{file_path}/cleaned_data_archives").mkdir(parents=True, exist_ok=True)


FileS3 = namedtuple("FileS3", ["key", "last_date", "size"])


def _retrieve_current_data_on_s3():

    s3 = boto3.resource("s3")
    all_files = s3.Bucket("checkercovid").objects.all()
    all_files = list(all_files)
    all_files_infos = [
        FileS3(f.key, f.last_modified, f.size) for f in all_files
    ]
    df_s3 = pd.DataFrame(all_files_infos)
    return df_s3


def get_current_latest_file_on_s3():
    filename = "all_EU.csv.gz"

    df = pd.DataFrame()
    try:
        # df_s3 = _retrieve_current_data_on_s3()
        # latest_file = df_s3[df_s3.last_date == df_s3.last_date.max()]
        # file_name = latest_file.iloc[0].key
        df = pd.read_csv(
            f"https://checkercovid.s3.amazonaws.com/{filename}",
            index_col=False,
        )
    except Exception as e:
        logging.error(f"{filename} not found in bucket ! ")
        logging.exception(e)
    return df


def upload_to_s3(updated_df, new_df, has_error=False):
    """[summary]

    [extended_summary]
    """
    # Let's use Amazon S3
    s3 = boto3.resource("s3")

    # Upload a new file adn add archive version :
    now = datetime.now()  # current date and time

    error_tag = "_error" if has_error else ""

    filename_archive_s3 = (
        f'all_EU_{now.strftime("%Y%m%d_%H_%M_%S")}{error_tag}.csv.gz'
    )
    filename_all_EU = f"all_EU{error_tag}.csv.gz"

    # store locally

    new_df.to_csv(
        pathlib.Path(file_path)
        / "cleaned_data_archives"
        / filename_archive_s3,
        index=False,
        compression="gzip",
    )

    updated_df.to_csv(
        pathlib.Path(file_path) / "cleaned_data_archives" / filename_all_EU,
        index=False,
        compression="gzip",
    )

    # upload cleaned df to s3
    data = open(
        f"{file_path}/cleaned_data_archives/{filename_archive_s3}", "rb"
    )
    s3.Bucket("checkercovid").put_object(Key=filename_archive_s3, Body=data)

    # upload latest to s3
    data = open(f"{file_path}/cleaned_data_archives/{filename_all_EU}", "rb")
    s3.Bucket("checkercovid").put_object(Key=filename_all_EU, Body=data)
