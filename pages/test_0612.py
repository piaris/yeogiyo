
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import time
import datetime
import requests
import apidata as api

conn = st.connection("final_project",type="sql")
df_seoulcity = conn.query("select * from Seoulcity")
df_predict = conn.query("select * from Predict")
# st.dataframe(df_predict)

# 한글폰트 설정
#print(plt.rcParams['font.family'])
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False


# css_file = "style.css"

# 혼잡도 예측 모델
AREA_NM = '강남역'
congest_result = '88.8%'
#congest_style = '<b style="font-family:serif; color:#8675FF; font-size: 60px;">📋congest_result </b>'
AREA_CONGEST_LVL = '보통'
AREA_CONGEST_MSG = '''사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.'''
AREA_PPLTN_MIN = '32000'
AREA_PPLTN_MAX = '34000'



# 1. default 강남 api값을 먼저 가져옴 default_ppltn

default_data = api.SeoulData("강남역")
default_ppltn = default_data.seoul_ppltn()
default_ppltn['AREA_PPLTN_median'] = default_ppltn[['AREA_PPLTN_MIN', 'AREA_PPLTN_MAX']].mean(axis=1)
st.dataframe(default_ppltn)
# default 혼잡지수 계산
default_congest = default_ppltn['AREA_PPLTN_median']
st.text(default_congest)

# 2. 원하는 날짜와 시간을 선택하세요
selected_date = '2024-06-04 11:00:00'
selected_time = '11:00:00'

# 3. 아래 카테고리에서 원하는 장소 1개 선택하세요, 워딩 포함만 되면 가져오기
selected_area = '서울대입구역'

# 4. 검색 장소키워드가 들어간 데이터프레임을 만드는 함수?
df_predict["PPLTN_TIME"] = pd.to_datetime(df_predict["PPLTN_TIME"])
df_predict_area = df_predict[
    (df_predict['AREA_NM'] == selected_area) &
    (df_predict['PPLTN_TIME'] == selected_date)
]
st.dataframe(df_predict_area)
st.text(df_predict_area['PREDICT'].values[0])

# 4. Predict table에서 비교해서 값을 가져옴




def find_area(input_area):
    return df.loc[df['AREA_NM'].str.contains(input_area), ['']]