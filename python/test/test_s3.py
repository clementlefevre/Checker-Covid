from services.s3_bucket import get_current_latest_file_on_s3
from config import COUNTRIES


def test_list_files_in_bucket():

    df_latest = get_current_latest_file_on_s3()
    delta_countries = list(set(df_latest.country.unique()) - set(COUNTRIES.keys()))
    print(delta_countries)
    assert len(delta_countries) == 2  # ['Emilia-Romagna', 'Lombardia']
