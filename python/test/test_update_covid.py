import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


from datetime import datetime
import pandas as pd
import boto3

from services.update_covid import update_all
from services.s3_bucket import get_current_latest_file_on_s3

import logging


def test_full_update(caplog):
    caplog.set_level(logging.INFO)
    df_current_s3 = get_current_latest_file_on_s3()
    update_all(["BE"])
    df_new_s3 = get_current_latest_file_on_s3()

    assert df_new_s3.shape[0] >= df_current_s3.shape[0]
