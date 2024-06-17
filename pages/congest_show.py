
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import xml.etree.ElementTree as ET
import sqldata as sqldata

# 기본설정 - 한글폰트
#print(plt.rcParams['font.family'])
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False
# 기본설정 - 디자인
# css_file = "style.css"

predict_df = sqldata.sql_predict()
st.dataframe(predict_df)

# 1. 모델 - *2주간의 예측 바+선그래프
# 2. 모델 - 추후 2주간의 예측 혼잡도 지수

#임시 데이터 입력
selected_area = "서울대입구역"
selected_date = "2024-06-13"
selected_time = "06"


def extract_congest(area):
    result = predict_df[(predict_df['AREA_NM'] == area)]
    return result[['PPLTN_TIME','PPLTN_DATE', 'PREDICT']]

predict_chart = extract_congest(selected_area)
st.dataframe(predict_chart)

# 혼잡도 예측 모델 임시 데이터
# AREA_NM = '강남역'
# congest_result = '88.8%'
# congest_style = '<b style="font-family:serif; color:#8675FF; font-size: 60px;">📋congest_result </b>'
# AREA_CONGEST_LVL = '보통'
# AREA_CONGEST_MSG = '''사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.'''
# AREA_PPLTN_MIN = '32000'
# AREA_PPLTN_MAX = '34000'


st.divider()

# # 5. api - 12시간 예측 바그래프

# if selected_date and selected_time and selected_area:

#     with st.container():
#         st.subheader(selected_area, '의 2주간의 예측 인구 그래프')
#         if predict_df['AREA_NM_ENG'] == selected_area:
#             predict_df['PREDICT']

#         chart_data1 = pd.DataFrame(
#             {

#             "예측시간" : list(predict_df['FCST_TIME']),
#             "유동인구(최소)" : predict_df['FCST_PPLTN_MIN'],
#             "유동인구(최대)" : predict_df['FCST_PPLTN_MAX']
#             }
#         )

#         st.bar_chart(chart_data1, x="예측시간", y=["유동인구(최소)", "유동인구(최대)"], color=['#8675FF','#FD7289'])

#     with st.container():
#         st.subheader(area_name, '의 연령별/성별 분포 그래프')

#         chart_data2 = pd.DataFrame(
#             {
#                 "최대 유동인구" : df_ppltn['AREA_PPLTN_MAX'],
#                 "최소 유동인구" : df_ppltn['AREA_PPLTN_MIN'],
#                 "남성 비율" : df_ppltn['MALE_PPLTN_RATE'],
#                 "여성 비율" : df_ppltn['FEMALE_PPLTN_RATE'],
#                 "10대" : df_ppltn['PPLTN_RATE_10'],
#                 "20대" : df_ppltn['PPLTN_RATE_20'],
#                 "30대" : df_ppltn['PPLTN_RATE_30'],
#                 "40대" : df_ppltn['PPLTN_RATE_40'],
#                 "50대" : df_ppltn['PPLTN_RATE_50'],
#                 "60대" : df_ppltn['PPLTN_RATE_60'],
#                 "70대" : df_ppltn['PPLTN_RATE_70']
#             }
#         )
#         st.dataframe(chart_data2)

#         bar_plot = plt.barh(chart_data2.columns, chart_data2.iloc[0])
#         st.pyplot(bar_plot)
# # # 6. api - 현재 연령 분포



