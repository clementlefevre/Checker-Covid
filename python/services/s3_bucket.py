import os
from pathlib import Path

from datetime import datetime
import pandas as pd
from collections import namedtuple
import boto3

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "data"))


Path(f"{file_path}/cleaned_data_archives").mkdir(parents=True, exist_ok=True)


FileS3 = namedtuple("FileS3", ["key", "last_date", "size"])


def _retrieve_current_data_on_s3():

    s3 = boto3.resource("s3")
    all_files = s3.Bucket("checkercovid").objects.all()
    all_files = list(all_files)
    all_files_infos = [FileS3(f.key, f.last_modified, f.size) for f in all_files]
    df_s3 = pd.DataFrame(all_files_infos)
    return df_s3


def get_current_latest_file_on_s3():

    df = pd.DataFrame()
    try:
        df_s3 = _retrieve_current_data_on_s3()
        latest_file = df_s3[df_s3.last_date == df_s3.last_date.max()]
        file_name = latest_file.iloc[0].key
        df = pd.read_csv(f"https://checkercovid.s3.amazonaws.com/{file_name}")
    except Exception as e:
        logging.error(f"{filename} not found in bucket ! ")
    return df


def upload_to_s3(updated_df, new_df):
    """[summary]

    [extended_summary]
    """
    # Let's use Amazon S3
    s3 = boto3.resource("s3")

    # Upload a new file adn add archive version :
    now = datetime.now()  # current date and time
    filename_archive_s3 = f'all_EU_{now.strftime("%Y%m%d_%H:%M:%S")}.csv'

    # store locally
    new_df.to_csv(
        f"{file_path}/cleaned_data_archives/{filename_archive_s3}", index=False
    )
    updated_df.to_csv(f"{file_path}/cleaned_data_archives/all_EU.csv", index=False)

    # upload cleaned df to s3
    data = open(f"{file_path}/cleaned_data_archives/{filename_archive_s3}", "rb")
    s3.Bucket("checkercovid").put_object(Key=filename_archive_s3, Body=data)

    # upload latest to s3
    data = open(f"{file_path}/cleaned_data_archives/all_EU.csv", "rb")
    s3.Bucket("checkercovid").put_object(Key="all_EU.csv", Body=data)
