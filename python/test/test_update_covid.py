import warnings


from services.update_covid import update_all
from services.s3_bucket import get_current_latest_file_on_s3

import logging
from main import main_job


warnings.simplefilter(action="ignore", category=FutureWarning)


def test_full_update(caplog):
    caplog.set_level(logging.INFO)
    df_current_s3 = get_current_latest_file_on_s3()
    update_all()
    df_new_s3 = get_current_latest_file_on_s3()

    assert df_new_s3.shape[0] >= df_current_s3.shape[0]


def test_job(caplog):
    caplog.set_level(logging.INFO)
    main_job()
