
import collections
from services.country_scrappers import *
from services.cleaner import (
    AT,
    BE,
    CH,
    DE,
    DK,
    SE,
    ES,
    PT,
    FR,
    IT,
    FI,
    EE,
    IE,
    NL,
    NO,
    OWID,
)

from services.scrapper import DK_scrap,FI_scrap,ES_scrap,NL_scrap


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

countries_data = {
    "AT": {
        "url": "https://info.gesundheitsministerium.at/data/data.zip",
        "url_apify": "https://api.apify.com/v2/datasets/EFWZ2Q5JAtC6QDSwV/items?format=json&clean=1",
        "scrapper": download_austria,
        "cleaner": AT.clean,
    },
    "BE": {
        "url": "https://epistat.sciensano.be/Data/COVID19BE.xlsx",
        "url_apify": "https://api.apify.com/v2/datasets/DD9jrAixr0QMvQIE3/items?format=json&clean=1",
        "scrapper": download_belgium,
        "cleaner": BE.clean,
    },
    "DK": {
        "url_sst_dk":"https://www.sst.dk/da/corona/tal-og-overvaagning",
        "url_apify": "https://api.apify.com/v2/datasets/Ugq8cNqnhUSjfJeHr/items?format=json&clean=1",
        "url_statista": "https://www.statista.com/statistics/1105720/patients-hospitalized-due-to-coronavirus-in-denmark/",
        "scrapper": DK_scrap.download_denmark,
        "cleaner": DK.clean,
    },
    "EE": {
        "url_spreadsheet": "https://docs.google.com/spreadsheets/d/1nGRqoWD6B8zXqBE7ftW2DG5sX9HNTu5FMoehBygLdg0/edit#gid=850749030",
        "url_apify": "https://api.apify.com/v2/datasets/Ix8h3SN2Ngyukf7yM/items?format=json&clean=1",
        "scrapper": download_estonia,
        "cleaner": EE.clean,
    },
    "FR": {
        "scrapper": download_france,
        "url_hospitalized_dept": "https://geodes.santepubliquefrance.fr/GC_refdata.php?nivgeo=dep&extent=fra&lang=fr&prodhash=3d7a4db9",
        "url_hospitalized_values": "https://geodes.santepubliquefrance.fr/GC_indic.php?lang=fr&prodhash=3d7a4db9&indic=hosp&dataset=covid_hospit&view=map2&filters=sexe=0,jour=",
        "url_icu_dept": "https://geodes.santepubliquefrance.fr/GC_refdata.php?nivgeo=dep&extent=fra&lang=fr&prodhash=78312ab6",
        "url_icu_values": "https://geodes.santepubliquefrance.fr/GC_indic.php?lang=fr&prodhash=78312ab6&indic=rea&dataset=covid_hospit&view=map2&filters=sexe=0,jour=",
        "url_test_dept": "https://geodes.santepubliquefrance.fr/GC_refdata.php?nivgeo=dep&extent=fra&lang=fr&prodhash=78312ab6",
        "url_test_values": "https://geodes.santepubliquefrance.fr/GC_indic.php?lang=fr&prodhash=78312ab6&indic=nb_test&dataset=covid_troislabo_quot&view=map2&filters=clage_covid=0,jour=",
        "cleaner": FR.clean,
    },
    "FI": {
        "url_apify": "https://api.apify.com/v2/datasets/BDEAOLx0DzEW91s5L/items?format=json&clean=1",
        "url_hospi_icu": "https://thl.fi/en/web/infectious-diseases/what-s-new/coronavirus-covid-19-latest-updates/situation-update-on-coronavirus",
        "scrapper": FI_scrap.download,
        "cleaner": FI.clean,
    },
    "DE": {
        "url_rki": "http://opendata.arcgis.com/agol/arcgis/dd4580c810204019a7b8eb3e0b329dd6/0.csv?",
        "url_total_cases": "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Fallzahl%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true",
        "url_icu_1": "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/",
        "url_icu_2": "-de.pdf?__blob=publicationFile",
        "url_esri_update_date": "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0?f=json",
        "scrapper": download_germany,
        "cleaner": DE.clean,
    },
    "ES": {
        #"url": "https://covid19.isciii.es/resources/serie_historica_acumulados.csv",
        "url_uclm":"https://covid19.esi.uclm.es/spain",
        "scrapper": ES_scrap.download,
        "cleaner": ES.clean,
    },
    "IE": {
        "url_1": "https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandView/FeatureServer/0/query?f=json&where=Date%3Ctimestamp%20%27",
        "url_2": "%2000:00:00%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=FID,TotalConfirmedCovidCases,HospitalisedCovidCases,RequiringICUCovidCases,Date&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true",
        "scrapper": download_ireland,
        "cleaner": IE.clean,
    },
    "IT": {
        "url": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
        "scrapper": download_italy,
        "cleaner": IT.clean,
    },
    "NL": {
        "url_global": "https://www.stichting-nice.nl/covid-19/public/global",
        "url_new_intake": "https://www.stichting-nice.nl/covid-19/public/new-intake/",
        "url_intake_count": "https://www.stichting-nice.nl/covid-19/public/intake-count/",
        "url_icu": "https://www.stichting-nice.nl/covid-19/public/ic-count/",
        "url_ic_cumulative": "https://www.stichting-nice.nl/covid-19/public/intake-cumulative/",
        "url_actuel": "https://www.rivm.nl/coronavirus-covid-19/actueel",
        "url_rivm" :"https://www.rivm.nl/coronavirus-covid-19/actueel",
        "scrapper": NL_scrap.download_netherland,
        "cleaner": NL.clean,
    },
    "NO": {
        "url_case": "https://www.fhi.no/en/id/infectious-diseases/coronavirus/daily-reports/daily-reports-COVID19/",
        "url_apify": "https://api.apify.com/v2/datasets/6tpTe4Z2TBePRWYti/items?format=json&clean=1",
        "scrapper": download_norway,
        "cleaner": NO.clean,
    },
    "OWID": {
        "url": "https://covid.ourworldindata.org/data/owid-covid-data.csv",
        "scrapper": download_owid,
        "cleaner": OWID.clean,
    },
    "PT": {
        "url_esri_1":"https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/An%C3%A1lises_Extra_Covid/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Data_do_Relat%C3%B3rio%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true",
        "url_esri_2":"https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19Portugal_view/FeatureServer/0/query?f=json&where=gr_etario_0_9%20IS%20NOT%20NULL&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=datarelatorio%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true",

        "scrapper": download_portugal,
        "cleaner": PT.clean,
    },
    "CH": {
        "url_apify": "https://api.apify.com/v2/datasets/73pVXuygDYAtIMOhI/items?format=json&clean=1",
        "scrapper": download_switzerland,
        "cleaner": CH.clean,
    },
    "SE": {
        "url_apify": "https://api.apify.com/v2/datasets/Nq3XwHX262iDwsFJS/items?format=json&clean=1",
        "url_current_icu": "https://www.icuregswe.org/data--resultat/covid-19-i-svensk-intensivvard/",
        "scrapper": download_sweden,
        "cleaner": SE.clean,
    },
}


COUNTRIES = collections.OrderedDict(sorted(countries_data.items()))
