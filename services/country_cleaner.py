import pandas as pd
from .covid import COVID

df_lookup = pd.read_csv("data/lookup.csv", sep=",")


def translate_and_select_cols(df, country):
    df_cols = pd.DataFrame(df.columns)
    df_cols.columns = ["original_field_name"]
    df_cols = pd.merge(
        df_cols, df_lookup[df_lookup["country"] == country], on="original_field_name"
    )
    df_cols = df_cols[~df_cols["tub_name"].isnull()]
    cols_translations = df_cols.to_dict(orient="records")
    original_cols_to_filter = [d["original_field_name"] for d in cols_translations]
    tub_cols_to_filter = [d["tub_name"] for d in cols_translations]
    df = df[original_cols_to_filter]
    df.columns = tub_cols_to_filter

    return df


def clean_austria():
    austria = COVID("austria")
    austria.scrapper()

    source_name = austria.params["url"]
    file_name = "AllgemeinDaten.csv"
    df = pd.read_csv(
        f"{austria.data_path}/raw/{austria.dt_created}/AllgemeinDaten.csv", sep=";"
    )

    df_translated = translate_and_select_cols(df, "austria")
    df_translated["updated_on"] = pd.to_datetime(df_translated["updated_on"]).dt.date
    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date

    df_global = pd.melt(
        df_translated,
        id_vars=["updated_on", "date"],
        value_vars=["tests", "curr_hospi", "curr_icu"],
        var_name="key",
        value_name="value",
    )

    df_global["source_url"] = source_name
    df_global["filename"] = file_name

    filename = "Epikurve.csv"
    df_cases = pd.read_csv(f"{austria.path_to_save}/{filename}", sep=";")
    df_cases = translate_and_select_cols(df_cases, "austria")
    df_cases["updated_on"] = pd.to_datetime(df_cases["updated_on"]).dt.date

    df_cases_melted = pd.melt(
        df_cases,
        id_vars=["updated_on", "date"],
        value_vars=["new_cases"],
        var_name="key",
        value_name="value",
    )

    df_cases_melted["source_url"] = source_name
    df_cases_melted["filename"] = filename

    df_autria_all = pd.concat([df_global, df_cases_melted], axis=0)
    df_autria_all["country"] = austria.country
    return df_autria_all


def clean_belgium():
    belgium = COVID("belgium")
    belgium.scrapper()

    filename = "COVID19BE.xlsx"
    source_file_path = f"{belgium.data_path}/raw/{belgium.dt_created}/{filename}"
    df_hosp = pd.read_excel(source_file_path, sheet_name="HOSP")
    df_hosp_group = df_hosp.groupby(["DATE"]).sum().reset_index()
    df = translate_and_select_cols(df_hosp_group, "belgium")
    df_melt = pd.melt(
        df,
        id_vars=["date"],
        value_vars=df.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melt["updated_on"] = pd.to_datetime(belgium.dt_created)
    df_melt["updated_on"] = df_melt["updated_on"].dt.date
    df_melt["source_url"] = belgium.params["url"]
    df_melt["filename"] = filename
    df_melt["country"] = belgium.country
    return df_melt


def clean_france():
    france = COVID("france")
    france.scrapper()

    filename_hosp = "total_hospitalized.csv"
    df_hosp = pd.read_csv(f"{france.data_path}/raw/{france.dt_created}/{filename_hosp}")
    df_hosp_translated = translate_and_select_cols(df_hosp, "france")
    df_hosp_translated = df_hosp_translated[df_hosp_translated["sex"] == 0]
    df_hosp_melted = pd.melt(
        df_hosp_translated,
        id_vars=["date"],
        value_vars=["curr_hospi"],
        var_name="key",
        value_name="value",
    )

    df_hosp_melted["source_url"] = france.params["url_hospitalized_values"]
    df_hosp_melted["filename"] = filename_hosp

    filename_icu = "total_icu.csv"
    df_icu = pd.read_csv(f"{france.data_path}/raw/{france.dt_created}/{filename_icu}")
    df_icu_tranlated = translate_and_select_cols(df_icu, "france")
    df_icu_tranlated = df_icu_tranlated[df_icu_tranlated["sex"] == 0]

    df_icu_melted = pd.melt(
        df_icu_tranlated,
        id_vars=["date"],
        value_vars=["curr_icu"],
        var_name="key",
        value_name="value",
    )

    df_icu_melted["source_url"] = france.params["url_icu_values"]
    df_icu_melted["filename"] = filename_icu
    df_icu_melted

    filename_tests = "total_test.csv"
    df_test = pd.read_csv(
        f"{france.data_path}/raw/{france.dt_created}/{filename_tests}"
    )
    df_test_translated = translate_and_select_cols(df_test, "france")

    df_test_melted = pd.melt(
        df_test_translated,
        id_vars=["date"],
        value_vars=["tested"],
        var_name="key",
        value_name="value",
    )

    df_test_melted["source_url"] = france.params["url_test_values"]
    df_test_melted["filename"] = filename_tests

    df_france = pd.concat([df_hosp_melted, df_icu_melted, df_test_melted], axis=0)
    df_france["updated_on"] = pd.to_datetime(france.dt_created)
    df_france["updated_on"] = df_france["updated_on"].dt.date
    df_france["country"] = france.country
    return df_france


def clean_germany():
    filename = "RKI.csv"
    germany = COVID("germany")
    germany.scrapper()
    df = pd.read_csv(f"{germany.path_to_save}/{filename}")

    groupy = df.groupby("Meldedatum").sum()

    groupy_cum = groupy.cumsum()
    groupy_cum.columns = ["cum_" + c for c in groupy.columns]

    df_all = pd.concat([groupy, groupy_cum], axis=1).reset_index()

    df_translated = translate_and_select_cols(df_all, "germany")
    df_translated["date"] = pd.to_datetime(df_translated["date"])
    df_translated["date"] = df_translated["date"].dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = germany.params["url_rki"]
    df_melted["updated_on"] = pd.to_datetime(germany.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = germany.country

    return df_melted


def clean_ireland():
    ireland = COVID("ireland")
    ireland.scrapper()

    filename = "total_cases_hospi_icu.csv"
    df = pd.read_csv(f"{ireland.data_path}/raw/{ireland.dt_created}/{filename}")
    df_translated = translate_and_select_cols(df, "ireland")

    df_translated["date"] = pd.to_datetime(df["Date"], unit="ms")

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=["cases", "curr_hospi", "curr_icu"],
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = (
        ireland.params["url_1"] + ireland.dt_created + ireland.params["url_2"]
    )
    df_melted["updated_on"] = pd.to_datetime(ireland.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = ireland.country

    return df_melted


def clean_italy():
    italy = COVID("italy")
    italy.scrapper()
    filename = "total.csv"

    italy.path_to_save

    df = pd.read_csv(f"{italy.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df, "italy")

    df_translated["date"] = pd.to_datetime(df_translated["date"]).dt.date

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=[
            "curr_icu",
            "curr_hospi",
            "new_cases",
            "cases",
            "tested",
            "cum_tests",
        ],
        var_name="key",
        value_name="value",
    )

    df_melted["updated_on"] = pd.to_datetime(italy.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = italy.country
    df_melted["source_url"] = italy.params["url"]

    return df_melted


def clean_portugal():
    portugal = COVID("portugal")
    portugal.scrapper()
    filename = "total.csv"
    df = pd.read_csv(f"{portugal.path_to_save}/{filename}")

    df_translated = translate_and_select_cols(df, "portugal")

    df_translated["date"] = pd.to_datetime(df_translated["date"], unit="ms")

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = portugal.params["url_esri_1"]
    df_melted["updated_on"] = pd.to_datetime(portugal.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = portugal.country

    return df_melted


def clean_spain():
    spain = COVID("spain")
    spain.scrapper()
    filename = "total.csv"
    df = pd.read_csv(f"{spain.path_to_save}/{filename}")

    df = df[~df["FECHA"].isnull()]
    df["FECHA"] = pd.to_datetime(df.FECHA, format="%d/%m/%Y")
    df.tail()

    groupy = df.groupby("FECHA").sum()

    groupy["cum_PCR+"] = groupy["PCR+"].diff()

    df_translated = translate_and_select_cols(groupy.reset_index(), "spain")

    df_melted = pd.melt(
        df_translated,
        id_vars=["date"],
        value_vars=df_translated.columns.tolist().remove("date"),
        var_name="key",
        value_name="value",
    )

    df_melted["source_url"] = spain.params["url"]
    df_melted["updated_on"] = pd.to_datetime(spain.dt_created)
    df_melted["updated_on"] = df_melted["updated_on"].dt.date
    df_melted["filename"] = filename
    df_melted["country"] = spain.country

    return df_melted

