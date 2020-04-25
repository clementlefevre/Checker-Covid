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
    "denmark": {
        "url_apify": "https://api.apify.com/v2/datasets/Ugq8cNqnhUSjfJeHr/items?format=json&clean=1",
        "scrapper": download_denmark,
    },
    "estonia": {
        "url_spreadsheet": "https://docs.google.com/spreadsheets/d/1nGRqoWD6B8zXqBE7ftW2DG5sX9HNTu5FMoehBygLdg0/edit#gid=850749030",
        "url_apify": "https://api.apify.com/v2/datasets/Ix8h3SN2Ngyukf7yM/items?format=json&clean=1",
        "scrapper": download_estonia,
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
    "finland": {
        "url_apify": "https://api.apify.com/v2/datasets/BDEAOLx0DzEW91s5L/items?format=json&clean=1",
        "scrapper": download_finland,
    },
    "germany": {
        "url_rki": "http://opendata.arcgis.com/agol/arcgis/dd4580c810204019a7b8eb3e0b329dd6/0.csv?",
        "url_total_cases": "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Fallzahl%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true",
        "url_icu_1": "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/",
        "url_icu_2": "-de.pdf?__blob=publicationFile",
        "url_esri_update_date": "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0?f=json",
        "scrapper": download_germany,
    },
    "ireland": {
        "url_1": "https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandView/FeatureServer/0/query?f=json&where=Date%3Ctimestamp%20%27",
        "url_2": "%2000:00:00%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=FID,TotalConfirmedCovidCases,HospitalisedCovidCases,RequiringICUCovidCases,Date&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true",
        "scrapper": download_ireland,
    },
    "italy": {
        "url": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
        "scrapper": download_italy,
    },
    "netherland": {
        "url_global": "https://www.stichting-nice.nl/covid-19/public/global",
        "url_new_intake": "https://www.stichting-nice.nl/covid-19/public/new-intake/",
        "url_intake_count": "https://www.stichting-nice.nl/covid-19/public/intake-count/",
        "url_icu": "https://www.stichting-nice.nl/covid-19/public/ic-count/",
        "url_ic_cumulative": "https://www.stichting-nice.nl/covid-19/public/intake-cumulative/",
        "url_actuel": "https://www.rivm.nl/coronavirus-covid-19/actueel",
        "scrapper": download_netherland,
    },
    "norway": {
        "url_case": "https://www.fhi.no/en/id/infectious-diseases/coronavirus/daily-reports/daily-reports-COVID19/",
        "url_apify": "https://api.apify.com/v2/datasets/6tpTe4Z2TBePRWYti/items?format=json&clean=1",
        "scrapper": download_norway,
    },
    "portugal": {
        "url_pdf_1": "https://covid19.min-saude.pt/wp-content/uploads/2020/04/51_DGS_boletim_20200422.pdf",
        "url_esri_1": "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/An%C3%A1lises_Extra_Covid/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Data_do_Relat%C3%B3rio%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true",
        "scrapper": download_portugal,
    },
    "spain": {
        "url": "https://covid19.isciii.es/resources/serie_historica_acumulados.csv",
        "scrapper": download_spain,
    },
    "switzerland": {
        "url_apify": "https://api.apify.com/v2/datasets/73pVXuygDYAtIMOhI/items?format=json&clean=1",
        "scrapper": download_switzerland,
    },
    "sweden": {
        "url_apify": "https://api.apify.com/v2/datasets/Nq3XwHX262iDwsFJS/items?format=json&clean=1",
        "scrapper": download_sweden,
    },
}
