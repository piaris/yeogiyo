import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from datetime import datetime, date, timedelta
import boto3
import requests
import logging

bucket_name = 'final-pjt-yeogiyo' # s3 bucket 이름
s3 = boto3.resource('s3')


def set_datetime(ti):
  now = datetime.now()
  now = now + timedelta(hours=9)
  now_date = now.strftime("%Y-%m-%d_%H:%M")
  ti.xcom_push(key='now_date', value=now_date)
  logging.info(now_date)



def request_congest_data(ti):
  data_df = pd.DataFrame()

  try :
    for i in range(1,116):
      url = "http://openapi.seoul.go.kr:8088/544259516c626f673332707066656a/json/citydata/1/5/POI"+f"{i}".zfill(3)
      response = requests.get(url)
      if response.status_code != 200:
        continue

      real_time_data = response.json()  # 서울시 실시간 도시데이터 전체

      if real_time_data.get("CITYDATA") == None:  # 서울시 실시간 도시 데이터 중 CITYDATA 부분이 없을 경우 넘어가기
        continue

      df = pd.DataFrame([real_time_data])
      data_df = pd.concat([data_df, df])

    buffer = BytesIO()
    table = pa.Table.from_pandas(data_df)
    pq.write_table(table, buffer)

    now_date = ti.xcom_pull(key='now_date')
    filename = f"congest_data_{now_date}.parquet"
    default_path = f'test/filename={filename}'
    # ti.xcom_push(key='df_congest', value=buffer.getvalue()

    obj = s3.Object(bucket_name, default_path)
    obj.put(Body=buffer.getvalue)
    logging.info(f'successed to upload tags_file! : {filename}')
    return {
    "successs" : "successs"
    }

  except Exception as e :
    logging.info("fail to request congest data")
    return {
      "fail" : "fail"
      }
