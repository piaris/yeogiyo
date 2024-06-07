import json
import boto3
import requests
import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO

now = datetime.datetime.now()
now = now + datetime.timedelta(hours=9)
start_date = now.strftime("%Y-%m-%d_%H:%M")

bucket = "final-project-playdata" # S3 버킷 이름
key = "crawling_congest_csv/data_%s.parquet" % start_date # S3 객체 키
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    data_df = pd.DataFrame()
    
    for i in range(1,116):
        url = "http://openapi.seoul.go.kr:8088/544259516c626f673332707066656a/json/citydata/1/5/POI"+f"{i}".zfill(3)
        response = requests.get(url)
        if response.status_code != 200:
            continue
        
        datav = response.json()
        if datav.get("CITYDATA") == None:
            continue
        
        df = pd.DataFrame([datav])
        data_df = pd.concat([data_df, df])
    
    buffer = BytesIO()
    table = pa.Table.from_pandas(data_df)
    pq.write_table(table, buffer)

    obj = s3.Object(bucket, key)
    obj.put(Body=buffer.getvalue())

    return {
        "successs" : "successs"
        }
    