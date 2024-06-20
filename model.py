import sqlalchemy
import numpy as np
import pandas as pd

engine = sqlalchemy.create_engine(
    "mysql+mysqldb://admin:rootroot@database-1.c3oywy0kww41.ap-northeast-2.rds.amazonaws.com/final_project",
    encoding="utf8",
)

sql = """
    SELECT AREA_NM, PPLTN_TIME, AREA_PPLTN_MIN, AREA_PPLTN_MAX, PPLTN_RATE_0, PPLTN_RATE_10, PPLTN_RATE_20, PPLTN_RATE_30, PPLTN_RATE_40, PPLTN_RATE_50, PPLTN_RATE_60, PPLTN_RATE_70 FROM Realtime;
"""

with engine.connect() as conn:
    df = pd.read_sql_query(sql, conn)

df_cp = df.copy()
AREA_NM_list = df_cp["AREA_NM"].unique()
df_cp[df_cp.columns[2:]] = df_cp[df_cp.columns[2:]].astype(float)

df_cp["ds"] = pd.to_datetime(df_cp["PPLTN_TIME"])
df_cp["DAY_NAME"] = df_cp["ds"].dt.day_name()
df_cp["PPLTN_DATE"] = pd.to_datetime(df_cp["PPLTN_TIME"]).dt.strftime("%Y-%m-%d")
df_cp["PPLTN_TIME"] = pd.to_datetime(df_cp["PPLTN_TIME"]).dt.strftime("%H")

df_cp["PREDICT"] = df_cp.loc[:, ["AREA_PPLTN_MIN", "AREA_PPLTN_MAX"]].sum(axis=1) / 2

for i in range(len(AREA_NM_list)):
    df_1 = df_cp[df_cp["AREA_NM"] == AREA_NM_list[i]].copy()
    df_1 = df_1.drop(["AREA_PPLTN_MIN", "AREA_PPLTN_MAX"], axis=1)
    tmp = df_1.groupby(["PPLTN_DATE", "PPLTN_TIME"], as_index=False).mean(
        df_1.columns[df_1.columns.str.contains("RATE")].to_list() + ["PREDICT"]
    )
    df_1.drop_duplicates(["PPLTN_DATE", "PPLTN_TIME"], inplace=True)
    df_1.reset_index(drop=True, inplace=True)
    df_1[df_1.columns[df_1.columns.str.contains("RATE")]] = tmp[
        tmp.columns[tmp.columns.str.contains("RATE")]
    ]
    df_1["PREDICT"] = tmp["PREDICT"]
    PPLTN_DATE_lst = df_1["PPLTN_DATE"].unique()[1:]

    for j in range(len(PPLTN_DATE_lst)):
        pre = df_1[df_1["ds"].dt.date < pd.to_datetime(PPLTN_DATE_lst[j]).date()]
        now = df_1[df_1["ds"].dt.date == pd.to_datetime(PPLTN_DATE_lst[j]).date()]
        group = (
            pre.drop(pre.columns[pre.columns.str.contains("RATE")], axis=1)
            .groupby(["DAY_NAME", "PPLTN_TIME"], as_index=False)
            .mean("PREDICT")
        )
        result = pd.merge(
            left=now,
            right=group,
            on=["DAY_NAME", "PPLTN_TIME"],
            suffixes=["", "_group"],
            how="left",
        )
        result["PERCENTAGE"] = round(result["PREDICT"] / result["PREDICT_group"] * 100)
        result.drop(columns=["PREDICT_group"], inplace=True)
        result["AREA_NM+PPLTN_TIME"] = (
            result["AREA_NM"] + "+" + result["PPLTN_DATE"] + " " + result["PPLTN_TIME"]
        )
        result = result.map(str)
        result_df = result.loc[
            :,
            [
                "AREA_NM+PPLTN_TIME",
                "AREA_NM",
                "PPLTN_DATE",
                "PPLTN_TIME",
                "DAY_NAME",
                "PREDICT",
                "PERCENTAGE",
                "PPLTN_RATE_0",
                "PPLTN_RATE_10",
                "PPLTN_RATE_20",
                "PPLTN_RATE_30",
                "PPLTN_RATE_40",
                "PPLTN_RATE_50",
                "PPLTN_RATE_60",
                "PPLTN_RATE_70",
            ],
        ]
        result_df.to_sql(
            name="Predict",
            con=engine,
            schema="final_project",
            if_exists="append",
            index=False,
            index_label="id",
            chunksize=1,
        )