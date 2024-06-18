
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

# selected_area = st.session_state.get('selected_area', )


if st.session_state:
    selected_area = st.session_state["selected_area"]
    selected_date = st.session_state["selected_date"]
    selected_time = st.session_state["selected_time"]

else:
    area = "강남역"

st.text(selected_area)
st.text(selected_date)

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



if selected_date and selected_time and selected_area:
    with st.container():
        st.subheader(selected_area, '의 연령별/성별 분포 그래프')

        chart_data2 = pd.DataFrame(
            {
                "예측일자" : predict_df['PPLTN_DATE'],
                "예측시간" : predict_df['PPLTN_TIME'],
                "요일" : predict_df['DAY_NAME'],
                "예상유동인구" : predict_df['PREDICT'],
                "10대" : predict_df['PPLTN_RATE_10'],
                "20대" : predict_df['PPLTN_RATE_20'],
                "30대" : predict_df['PPLTN_RATE_30'],
                "40대" : predict_df['PPLTN_RATE_40'],
                "50대" : predict_df['PPLTN_RATE_50'],
                "60대" : predict_df['PPLTN_RATE_60'],
                "70대" : predict_df['PPLTN_RATE_70']
            }
        )
        st.dataframe(chart_data2)

        bar_plot = plt.barh(chart_data2.columns, chart_data2.iloc[0])
        st.pyplot(bar_plot)
        st.bar_chart(chart_data2.iloc[:,4:].T)
# # # 6. api - 현재 연령 분포



