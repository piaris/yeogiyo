import os
import re
import boto3
import logging
from io import BytesIO
from dotenv import load_dotenv

from datetime import datetime
import pymysql
import mysql.connector
from mysql.connector import Error

import pandas as pd
import pyarrow.parquet as pq



# 글로벌 변수 설정 : AWS info
AWS_ACCESS_KEY_ID =os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET_NAME="final-project-playdata"
PREFIX="crawling_congest_csv/"



# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('insert_tags_data.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)




# s3로부터 object list 가져오기
def get_object_list():
    global BUCKET_NAME
    global PREFIX

    try:
        s3 = boto3.client('s3')
        obj_data = s3.list_objects(Bucket=BUCKET_NAME, Prefix=PREFIX)
        contents_list = obj_data.get('Contents', [])
        object_list = []

        for content in contents_list:
            file_name = content['Key']
            if file_name.endswith(".json"):
                object_list.append(file_name)

        return object_list
    except Exception as e:
        logging.error(f"Error retrieving object list from S3: {str(e)}")
        return []




# RDS(mysql)과 연결
def set_mysql_conn():
  try:
    connection = mysql.connector.connect(
      host=os.getenv('HOST'),
      user=os.getenv('USER'),
      password=os.getenv('PASSWORD'),
      database=os.getenv('DB'),
      charset=os.getenv('CHARSET')
    )
    if connection.is_connected():
      logging.info('MySQL 데이터베이스 연결 성공')
      return connection
  except Exception as e:
      logging.error(f'MySQL 에러: {str(e)}')
  return None



# 필터링된 객체 리스트 가져오기
def filtered_object_list() :
  try:
    # mysql 연결
    connection = set_mysql_conn()
    if connection is None:
        return []
    cursor = connection.cursor()

    # 저장된 file 내용 filter (기준 : PPLTN_TIME)
    sql = 'SELECT DISTINCT PPLTN_TIME FROM Realtime'
    cursor.execute(sql)
    existing_data = set(row[0] for row in cursor.fetchall())
    filtered_object = []
    object_list = get_object_list()

    # 필터링 작업
    pattern = r"(\d{4}-\d{2}-\d{2})_(\d{2}:\d{2})"
    for object_key in object_list:
      match = re.search(pattern, object_key)
      if match:
        datetime_str = f'{match.group(1)} {match.group(2)}'
        if datetime_str not in existing_data:
          filtered_object.append(object_key)

        cursor.close()
        connection.close()
    logging.info(f'Filtered object list: {filtered_object}')
    return filtered_object

  except Exception as e:
    logging.error(f"Error filtering object list: {str(e)}")
    return []





def insert_congest_data():
  # mysql connection
  try:
    connection = set_mysql_conn()
    if connection is None:
      return

    cursor = connection.cursor()
    filtered_object = filtered_object_list()
    s3 = boto3.client('s3')

    # 저장할 parquet object list
    filtered_object = filtered_object_list()


    s3 = boto3.client('s3')
    for object_key in filtered_object:
      # S3에서 parquet object 가져오기
      s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
      parquet_data = s3_object['Body'].read()
      parquet_stream = BytesIO(parquet_data)
      df = pd.read_parquet(parquet_stream)
      # table = pq.read_table(parquet_stream)
      # df = table.to_pandas()
      for  i in range(len(df)) :
        try:
          df_dict = df.iloc[i].to_dict()
          # Realtime data
          AREA_CD_PPLTN_TIME = df_dict["CITYDATA"]["AREA_CD"]+"+"+df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_TIME"]
          AREA_NM = df_dict["CITYDATA"]["AREA_NM"]

          # LIVE_PPLTN_STTS data
          AREA_CONGEST_LVL = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_CONGEST_LVL"]
          AREA_CONGEST_MSG = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_CONGEST_MSG"]
          PPLTN_TIME = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_TIME"]
          AREA_PPLTN_MIN = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_PPLTN_MIN"]
          AREA_PPLTN_MAX = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["AREA_PPLTN_MAX"]
          MALE_PPLTN_RATE = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["MALE_PPLTN_RATE"]
          FEMALE_PPLTN_RATE = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FEMALE_PPLTN_RATE"]
          PPLTN_RATE_0 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_0"]
          PPLTN_RATE_10 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_10"]
          PPLTN_RATE_20 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_20"]
          PPLTN_RATE_30 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_30"]
          PPLTN_RATE_40 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_40"]
          PPLTN_RATE_50 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_50"]
          PPLTN_RATE_60 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_60"]
          PPLTN_RATE_70 = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_RATE_70"]

          # ROAD_TRAFFIC_STTS data
          if df_dict["CITYDATA"].get("ROAD_TRAFFIC_STTS") == None or df_dict["CITYDATA"]["ROAD_TRAFFIC_STTS"].get("AVG_ROAD_DATA") == None:
              ROAD_TRAFFIC_IDX,ROAD_MSG,ROAD_TRFFIC_TIME,ROAD_TRAFFIC_SPD=[None]*4
          else:
              ROAD_TRAFFIC_IDX = df_dict["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_TRAFFIC_IDX"]
              ROAD_MSG = df_dict["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_MSG"]
              ROAD_TRFFIC_TIME = df_dict["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_TRFFIC_TIME"]
              ROAD_TRAFFIC_SPD = df_dict["CITYDATA"]["ROAD_TRAFFIC_STTS"]["AVG_ROAD_DATA"]["ROAD_TRAFFIC_SPD"]

          # Realtime_FCST data
          AREA_NM_FCST_TIME = df_dict["CITYDATA"]["AREA_NM"]+"+"+df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_TIME"]
          AREA_NM
          FCST_TIME = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_TIME"]
          FCST_CONGEST_LVL = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_CONGEST_LVL"]
          FCST_PPLTN_MIN = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_PPLTN_MIN"]
          FCST_PPLTN_MAX = df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["FCST_PPLTN"][0]["FCST_PPLTN_MAX"]
          PPLTN_TIME

          # Congest data
          AREA_NM_PPLTN_TIME = df_dict["CITYDATA"]["AREA_NM"]+"+"+df_dict["CITYDATA"]["LIVE_PPLTN_STTS"][0]["PPLTN_TIME"]
          AREA_NM
          AREA_PPLTN_MEDIAN = sum(map(int, [AREA_PPLTN_MAX, AREA_PPLTN_MIN]))/2
          AREA_PPLTN_MAX
          AREA_PPLTN_MIN
          AREA_CONGEST_LVL
          PPLTN_TIME


          # Realtime table 삽입
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
          cursor.execute(SQL,param)

          # Congest table 삽입
          param = AREA_NM_PPLTN_TIME,AREA_NM,AREA_PPLTN_MEDIAN,AREA_PPLTN_MAX,AREA_PPLTN_MIN,AREA_CONGEST_LVL,PPLTN_TIME
          SQL = """
          INSERT IGNORE INTO Congest (`AREA_NM+PPLTN_TIME`,AREA_NM,AREA_PPLTN_MEDIAN,AREA_PPLTN_MAX,AREA_PPLTN_MIN,AREA_CONGEST_LVL,PPLTN_TIME)\
          VALUES(%s,%s,%s,%s,%s,%s,%s)
          """
          cursor.execute(SQL,param)
          connection.commit()
        except Exception as e:
          logging.error(f"S3 객체 {object_key} 처리 중 오류 발생: {str(e)}")

    cursor.close()
    connection.close()
    logging.info("데이터 삽입 완료")

  except Exception as e:
      logging.error(f"insert_congest_data 함수 실행 중 오류 발생: {str(e)}")





def insert_tags_data(filename):
  # tag data 파일 불러오기
  try:
    # tag data 파일 불러오기
    df = pd.read_csv(filename, sep='[')
    logging.info('CSV 파일을 성공적으로 불러왔습니다.')

    # index, column 재설정
    df.columns = ['tags']
    df["tags"] = df["tags"].str[:-1]
    df.index = df.index.str[:-1]
    df_tags = df

    # loc('AREA_NM) 정보 추가
    temp = pd.read_excel('data/서울시115장소명 목록_장소명수정_20240527.xlsx', usecols=['AREA_NM'])
    temp.set_index(df_tags.index, inplace=True)
    df_tags['loc'] = temp
    logging.info('엑셀 파일을 성공적으로 불러왔습니다.')

    # mysql 연결
    conn = set_mysql_conn()
    cur = conn.cursor()
    logging.info('MySQL에 성공적으로 연결되었습니다.')


    # query 실행
    date = datetime.now().strftime('%Y-%m-%d')
    concat_date = date.replace('-', '')
    for index, row in df_tags.iterrows():
      row_tags = row['tags'].split(',')
      loc = row['loc']
      for tag in row_tags :
      # SQL 쿼리 실행
        query = f"INSERT INTO Naver (AREA_SEARCH, AREA_NM, HASHTAG, UPDATE_DATE) \
                VALUES ('{index}', '{loc}', '{tag.strip()}', '{date}')"
        cur.execute(query)
        logging.info(f"데이터 삽입 성공: {index}, {loc}, {tag.strip()}, {date}")

# 변경 사항 저장 및 연결 닫기
    conn.commit()
    logging.info('데이터베이스 커밋 완료.')

  except Exception as e:
      logging.error(f'오류 발생: {e}')

  finally:
    conn.close()
    logging.info('MySQL 연결이 닫혔습니다.')

