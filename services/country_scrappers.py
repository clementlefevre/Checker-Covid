import requests
import re
import pandas  as pd
from zipfile import ZipFile
from io import BytesIO,StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

from pathlib import Path
import pygsheets
from tabula import read_pdf

from lxml import html
from pathlib import Path


from datetime import datetime,timedelta


now = datetime.now() # current date and time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def download_zip(file_url, target_path):
    url = requests.get(file_url)
    zipfile = ZipFile(BytesIO(url.content))
    with zipfile as zip_ref:
        zip_ref.extractall(target_path)
        
def download_austria(covid):
    path_to_save = f"{covid.data_path}/raw/{covid.dt_created}"
    Path(path_to_save).mkdir(parents=True, exist_ok=True)  
    download_zip(covid.params['url'], path_to_save)
    

def download_belgium(covid):
    response = requests.get(covid.params['url'])
    path_to_save = f"{covid.data_path}/raw/{covid.dt_created}"
    Path(path_to_save).mkdir(parents=True, exist_ok=True)  
    with open(f'{path_to_save}/COVID19BE.xlsx', 'wb') as f:
        f.write(response.content)


#could not find total cases
def download_france_total(covid,url_dept,url_values,field):
    path_to_save = f"{covid.data_path}/raw/{covid.dt_created}"
    date = now.strftime("%Y-%m-%d")
    url_values = url_values+now.strftime("%Y-%m-%d")

    response_values = requests.get(url_values,headers=headers)
    
    df = pd.DataFrame(response_values.json()['content']['zonrefs'][0]['values'])
    if field !='test':
        df = df[df.sexe=='0']
    else:
        df = df[df.clage_covid=='0'].groupby('jour').sum().reset_index()
    
    Path(path_to_save).mkdir(parents=True, exist_ok=True)  
    df.to_csv(f'{path_to_save}/total_{field}.csv')  
    
def download_france(covid):
    download_france_total(covid,covid.params['url_icu_dept'],covid.params['url_icu_values'],'icu')
    download_france_total(covid,covid.params['url_hospitalized_dept'],covid.params['url_hospitalized_values'],'hospitalized')
    download_france_total(covid,covid.params['url_test_dept'],covid.params['url_test_values'],'test')

