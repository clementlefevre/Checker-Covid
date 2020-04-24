import pandas as pd
from .covid import COVID

df_lookup = pd.read_csv("data/lookup.csv", sep=",")


def clean_austria():
    austria = COVID("austria")
    austria.scrapper()

    source_name = austria.params["url"]
    file_name = "AllgemeinDaten.csv"
    df = pd.read_csv(
        f"{austria.data_path}/raw/{austria.dt_created}/AllgemeinDaten.csv", sep=";"
    )
    df = df.T

    df.columns = ["value"]

    df["country"] = "austria"
    df = df.reset_index().rename(columns={"index": "original_field_name"})

    df_austria = pd.merge(df_lookup, df, on=["country", "original_field_name"])
    df_austria = df_austria[~df_austria["tub_name"].isnull()]
    df_austria["retrieved_on"] = austria.dt_created
    df_austria["date"] = df_austria[
        df_austria["original_field_name"] == "Timestamp"
    ].iloc[0]["value"]
    df_austria["source_url"] = source_name
    df_austria["file_name"] = file_name

    return df_austria


def clean_belgium():
    belgium = COVID("belgium")
    belgium.scrapper()

    source_file_path = f"{belgium.data_path}/raw/{belgium.dt_created}/COVID19BE.xlsx"
    df_hosp = pd.read_excel(source_file_path, sheet_name="HOSP")
    date = df_hosp.tail(1).iloc[0]["DATE"]
    df_hosp = df_hosp.groupby(["DATE"]).sum().tail(1).T.reset_index()
    df_hosp.columns = ["original_field_name", "value"]
    df_hosp["retrieved_on"] = belgium.dt_created
    df_hosp = pd.merge(df_lookup, df_hosp, on="original_field_name")
    df_hosp = df_hosp[~df_hosp["tub_name"].isnull()]
    df_hosp["date"] = date
    df_hosp

    cum_cases_sheet_name = "CASES_MUNI_CUM"
    df_BE_cum_cases = pd.read_excel(source_file_path, sheet_name=cum_cases_sheet_name)
    # # cumulated cases, !!! we replace <5 with 3:
    df_BE_cum_cases["CASES"] = (
        df_BE_cum_cases["CASES"].str.replace("<5", "3").astype(int)
    )
    cum_cases = df_BE_cum_cases[~df_BE_cum_cases["NIS5"].isna()]["CASES"].sum()
    df_cases = pd.DataFrame(
        [{"country": "belgium", "tub_name": "cases", "value": cum_cases}]
    )
    df_cases["retrieved_on"] = belgium.dt_created
    df_cases["date"] = date
    df_cases["original_field_name"] = f"sum_of_sheet_{cum_cases_sheet_name}"

    cum_test_sheet_name = "TESTS"
    df_test = pd.read_excel(source_file_path, sheet_name=cum_test_sheet_name)
    df_test = df_test.tail(1)
    df_test.columns = ["date", "value"]
    df_test["tub_name"] = "tests"
    df_test["country"] = "belgium"
    df_test["retrieved_on"] = belgium.dt_created
    df_test["original_field_name"] = f"sum_of_sheet_{cum_test_sheet_name}"

    df = pd.concat([df_cases, df_test, df_hosp], axis=0)

    return df


def clean_france():
    france = COVID("france")
    france.scrapper()
    df_hosp = pd.read_csv(
        f"{france.data_path}/raw/{france.dt_created}/total_hospitalized.csv"
    )
    df_hosp = df_hosp.tail(1)[["jour", "hosp"]]
    df_hosp["tub_name"] = "cases"
    df_hosp.columns = ["date", "value", "tub_name"]
    df_icu = pd.read_csv(f"{france.data_path}/raw/{france.dt_created}/total_icu.csv")
    df_icu = df_icu.tail(1)[["jour", "rea"]]
    df_icu["tub_name"] = "curr_icu"
    df_icu.columns = ["date", "value", "tub_name"]
    df_test = pd.read_csv(f"{france.data_path}/raw/{france.dt_created}/total_test.csv")
    df_test = df_test.tail(1)[["jour", "nb_test"]]
    df_test["tub_name"] = "tests"
    df_test.columns = ["date", "value", "tub_name"]
    df = pd.concat([df_hosp, df_icu, df_test], axis=0)
    df["country"] = "france"
    return df


def clean_ireland():
    ireland = COVID("ireland")
    ireland.scrapper()
    df = pd.read_csv(
        f"{ireland.data_path}/raw/{ireland.dt_created}/total_cases_hospi_icu.csv"
    )
    df = df.tail(1).T.reset_index()
    df.columns = ["original_field_name", "value"]
    df = pd.merge(df, df_lookup, on="original_field_name")
    df["retrieved_on"] = ireland.dt_created
    df["source_url"] = (
        ireland.params["url_1"] + ireland.dt_created + ireland.params["url_2"]
    )
    df["file_name"] = "total_cases_hospi_icu.csv"

    return df
