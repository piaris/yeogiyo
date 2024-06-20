import pymysql
import boto3
import json
import os
from dotenv import load_dotenv

AWS_ACCESS_KEY_ID =os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET_NAME="final-project-playdata"
PREFIX="crawling_congest_csv/"

HOST=os.getenv('HOST'),
USER=os.getenv('USER'),
PASSWORD=os.getenv('PASSWORD'),
DB=os.getenv('DB'),
CHARSET=os.getenv('CHARSET')

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION)

list_obj = s3_client.list_objects(Bucket=BUCKET_NAME, Prefix=PREFIX)["Contents"][1:]
list_json = []
for j in range(len(list_obj)):
    if list_obj[j]["Key"].endswith("json"):
        list_json.append(list_obj[j]["Key"])

conn = pymysql.connect(
    host=HOST, user=USER, password=PASSWORD,
    db=DB, charset=CHARSET)
cur = conn.cursor()

for i in range(len(list_json)):
    jd = json.loads(s3_client.get_object(Bucket=BUCKET_NAME, Key=list_json[i])["Body"].read().decode())
    KEY=list_json[i]
    for j in range(len(jd)):
        CODE = list(jd.keys())[j]
        if jd[CODE].get("CITYDATA") == None:
            continue
        # Realtime
        AREA_CD_PPLTN_TIME = jd[CODE]["CITYDATA"]["AREA_CD"]+"+"+jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_TIME"]
        AREA_NM = jd[CODE]["CITYDATA"]["AREA_NM"]

        # LIVE_PPLTN_STTS
        AREA_CONGEST_LVL = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_CONGEST_LVL"]
        AREA_CONGEST_MSG = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_CONGEST_MSG"]
        PPLTN_TIME = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_TIME"]
        AREA_PPLTN_MIN = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_PPLTN_MIN"]
        AREA_PPLTN_MAX = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_PPLTN_MAX"]
        MALE_PPLTN_RATE = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["MALE_PPLTN_RATE"]
        FEMALE_PPLTN_RATE = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FEMALE_PPLTN_RATE"]
        PPLTN_RATE_0 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_0"]
        PPLTN_RATE_10 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_10"]
        PPLTN_RATE_20 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_20"]
        PPLTN_RATE_30 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_30"]
        PPLTN_RATE_40 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_40"]
        PPLTN_RATE_50 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_50"]
        PPLTN_RATE_60 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_60"]
        PPLTN_RATE_70 = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_70"]

        # ROAD_TRAFFIC_STTS
        if jd[CODE]["CITYDATA"].get("ROAD_TRAFFIC_STTS") == None or jd[CODE]["CITYDATA"]["ROAD_TRAFFIC_STTS"].get("AVG_ROAD_DATA") == None:
            ROAD_TRAFFIC_IDX,ROAD_MSG,ROAD_TRFFIC_TIME,ROAD_TRAFFIC_SPD=[None]*4
        else:
            ROAD_TRAFFIC_IDX = jd[CODE]["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_TRAFFIC_IDX"]
            ROAD_MSG = jd[CODE]["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_MSG"]
            ROAD_TRFFIC_TIME = jd[CODE]["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_TRFFIC_TIME"]
            ROAD_TRAFFIC_SPD = jd[CODE]["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_TRAFFIC_SPD"]

        # Realtime_FCST
        AREA_NM_FCST_TIME = jd[CODE]["CITYDATA"]["AREA_NM"]+"+"+jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_TIME"]
        AREA_NM
        FCST_TIME = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_TIME"]
        FCST_CONGEST_LVL = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_CONGEST_LVL"]
        FCST_PPLTN_MIN = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_PPLTN_MIN"]
        FCST_PPLTN_MAX = jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_PPLTN_MAX"]
        PPLTN_TIME

        # Congest
        AREA_NM_PPLTN_TIME = jd[CODE]["CITYDATA"]["AREA_NM"]+"+"+jd[CODE]["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_TIME"]
        AREA_NM
        AREA_PPLTN_MEDIAN = sum(map(int, [AREA_PPLTN_MAX, AREA_PPLTN_MIN]))/2
        AREA_PPLTN_MAX
        AREA_PPLTN_MIN
        AREA_CONGEST_LVL
        PPLTN_TIME

        param = AREA_CD_PPLTN_TIME,AREA_NM,AREA_CONGEST_LVL,AREA_CONGEST_MSG,\
        PPLTN_TIME,AREA_PPLTN_MIN,AREA_PPLTN_MAX,MALE_PPLTN_RATE,FEMALE_PPLTN_RATE,\
        PPLTN_RATE_0,PPLTN_RATE_10,PPLTN_RATE_20,PPLTN_RATE_30,PPLTN_RATE_40,PPLTN_RATE_50,\
        PPLTN_RATE_60,PPLTN_RATE_70,ROAD_TRAFFIC_IDX,ROAD_MSG,ROAD_TRFFIC_TIME,ROAD_TRAFFIC_SPD
        SQL = """
        INSERT IGNORE INTO Realtime (`AREA_CD+PPLTN_TIME`,AREA_NM,AREA_CONGEST_LVL,AREA_CONGEST_MSG,\
        PPLTN_TIME,AREA_PPLTN_MIN,AREA_PPLTN_MAX,MALE_PPLTN_RATE,FEMALE_PPLTN_RATE,\
        PPLTN_RATE_0,PPLTN_RATE_10,PPLTN_RATE_20,PPLTN_RATE_30,PPLTN_RATE_40,PPLTN_RATE_50,\
        PPLTN_RATE_60,PPLTN_RATE_70,ROAD_TRAFFIC_IDX,ROAD_MSG,ROAD_TRFFIC_TIME,ROAD_TRAFFIC_SPD)\
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(SQL,param)

        param = AREA_NM_FCST_TIME,AREA_NM,FCST_TIME,FCST_CONGEST_LVL,FCST_PPLTN_MIN,FCST_PPLTN_MAX,PPLTN_TIME
        SQL = """
        INSERT IGNORE INTO Realtime_FCST (`AREA_NM+FCST_TIME`,AREA_NM,FCST_TIME,FCST_CONGEST_LVL,FCST_PPLTN_MIN,FCST_PPLTN_MAX,PPLTN_TIME)\
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(SQL,param)

        param = AREA_NM_PPLTN_TIME,AREA_NM,AREA_PPLTN_MEDIAN,AREA_PPLTN_MAX,AREA_PPLTN_MIN,AREA_CONGEST_LVL,PPLTN_TIME
        SQL = """
        INSERT IGNORE INTO Congest (`AREA_NM+PPLTN_TIME`,AREA_NM,AREA_PPLTN_MEDIAN,AREA_PPLTN_MAX,AREA_PPLTN_MIN,AREA_CONGEST_LVL,PPLTN_TIME)\
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(SQL,param)
        conn.commit()

cur.close()
conn.close()