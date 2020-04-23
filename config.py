from services.country_scrappers import *

COUNTRIES = {
    "austria": {
        "url": "https://info.gesundheitsministerium.at/data/data.zip",
        "scrapper": download_austria,
    },
    "belgium": {
        "url": "https://epistat.sciensano.be/Data/COVID19BE.xlsx",
        "scrapper": download_belgium,
    },
    "estonia": {
        "url": "https://docs.google.com/spreadsheets/d/1nGRqoWD6B8zXqBE7ftW2DG5sX9HNTu5FMoehBygLdg0/edit#gid=0"
    },
    "france": {
       "scrapper": download_france,
        "url_hospitalized_dept": "https://geodes.santepubliquefrance.fr/GC_refdata.php?nivgeo=dep&extent=fra&lang=fr&prodhash=3d7a4db9",
        "url_hospitalized_values": "https://geodes.santepubliquefrance.fr/GC_indic.php?lang=fr&prodhash=3d7a4db9&indic=hosp&dataset=covid_hospit&view=map2&filters=sexe=0,jour=",
        "url_icu_dept": "https://geodes.santepubliquefrance.fr/GC_refdata.php?nivgeo=dep&extent=fra&lang=fr&prodhash=78312ab6",
        "url_icu_values": "https://geodes.santepubliquefrance.fr/GC_indic.php?lang=fr&prodhash=78312ab6&indic=rea&dataset=covid_hospit&view=map2&filters=sexe=0,jour=",
        "url_test_dept": "https://geodes.santepubliquefrance.fr/GC_refdata.php?nivgeo=dep&extent=fra&lang=fr&prodhash=78312ab6",
        "url_test_values": "https://geodes.santepubliquefrance.fr/GC_indic.php?lang=fr&prodhash=78312ab6&indic=nb_test&dataset=covid_troislabo_quot&view=map2&filters=clage_covid=0,jour=",
    },
    "germany": {
        "url_total_cases": "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Fallzahl%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true",
        "url_icu_1": "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/",
        "url_icu_2": "-de.pdf?__blob=publicationFile",
    },
    "ireland": {
        "url_total_cases_1": "https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandView/FeatureServer/0/query?f=json&where=Date%3Ctimestamp%20%27",
        "url_total_cases_2": "%2022%3A00%3A00%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=FID%2CTotalConfirmedCovidCases%2CDate&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true",
        "url_hospitalization_icu_1": "https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandView/FeatureServer/0/query?f=json&where=StatisticsProfileDate%3E%3Dtimestamp%20%27",
        "url_hospitalization_icu_2": "%2022%3A00%3A00%27%20AND%20StatisticsProfileDate%3C%3Dtimestamp%20%272020-04-19%2021%3A59%3A59%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22HospitalisedCovidCases%22%2C%22outStatisticFieldName%22%3A%22HospitalisedCovidCases%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22RequiringICUCovidCases%22%2C%22outStatisticFieldName%22%3A%22RequiringICUCovidCases%22%7D%5D&resultType=standard&cacheHint=true",
    },
    "italy": {
        "url": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
    },
    "netherland": {
        "url_global": "https://www.stichting-nice.nl/covid-19/public/global",
        "url_new_intake": "https://www.stichting-nice.nl/covid-19/public/new-intake/",
        "url_intake_count": "https://www.stichting-nice.nl/covid-19/public/intake-count/",
        "url_icu": "https://www.stichting-nice.nl/covid-19/public/ic-count/",
        "url_ic_count": "https://www.stichting-nice.nl/covid-19/public/ic-count/",
        "url_actuel": "https://www.rivm.nl/coronavirus-covid-19/actueel",
    },
    "norway": {
        "url_case": "https://www.fhi.no/en/id/infectious-diseases/coronavirus/daily-reports/daily-reports-COVID19/"
    },
    "portugal": {
        "url_pdf_1": "https://covid19.min-saude.pt/wp-content/uploads/2020/04/51_DGS_boletim_20200422.pdf",
        "url_esri_1": "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19Portugal_UltimoRel/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true",
    },
    "spain": {
        "url_start": "https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm",
    },
}
