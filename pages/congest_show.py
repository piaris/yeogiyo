
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import xml.etree.ElementTree as ET
import sqldata as sqldata
import datetime

# 기본설정 - 한글폰트
#print(plt.rcParams['font.family'])
plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams['axes.unicode_minus'] = False
# 기본설정 - 디자인
# css_file = "style.css"

predict_df = sqldata.sql_predict()
# st.dataframe(predict_df)

# 1. 모델 - *2주간의 예측 바+선그래프
# 2. 모델 - 추후 2주간의 예측 혼잡도 지수

# selected_area = st.session_state.get('selected_area', )

if st.session_state:
    selected_area = st.session_state["selected_area"]
    selected_date = str(st.session_state["selected_date"])
    selected_time = str(st.session_state["selected_time"]).zfill(2)

else:
    selected_area = "강남역"
    selected_date = "2024-06-10"
    selected_time = "00"    

    st.session_state["selected_area"] = selected_area
    st.session_state["selected_date"] = selected_date
    st.session_state["selected_time"] = selected_time
    
st.text(selected_area)
st.text(selected_date)
st.text(selected_time+":00")

def extract_congest(area):
    result = predict_df[(predict_df['AREA_NM'] == area)]
    return result[['PPLTN_TIME','PPLTN_DATE', 'PREDICT']]

predict_chart = extract_congest(selected_area)
predict_chart.drop_duplicates(inplace=True)

cond1 = predict_chart["PPLTN_DATE"] >= selected_date
cond2 = predict_chart["PPLTN_DATE"] <= str(pd.to_datetime(selected_date)+datetime.timedelta(days=14))
print(str(pd.to_datetime(selected_date)+datetime.timedelta(days=14)))
cond3 = predict_chart["PPLTN_TIME"] == selected_time
bar = predict_chart[cond1 & cond2 & cond3]
if len(bar) > 0:
    fig = plt.figure()
    bar_plot = plt.plot(bar["PPLTN_DATE"], bar["PREDICT"].map(float))
    plt.xticks(rotation=45)
    plt.ylim(0,max(bar["PREDICT"].map(float))*1.1)
    st.pyplot(fig)


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

        cond1 = predict_df["PPLTN_DATE"] >= selected_date
        cond2 = predict_df["PPLTN_DATE"] <= str(pd.to_datetime(selected_date)+datetime.timedelta(days=14))
        print(str(pd.to_datetime(selected_date)+datetime.timedelta(days=14)))
        cond3 = predict_df["PPLTN_TIME"] == selected_time
        chart = predict_df[cond1 & cond2 & cond3].copy()
        chart.drop_duplicates(subset=["PPLTN_DATE"],inplace=True)
        chart.sort_values(by="PPLTN_DATE", inplace=True)
        chart.reset_index(drop=True, inplace=True)

        chart_data2 = pd.DataFrame(
            {
                "예측일자" : chart['PPLTN_DATE'],
                "예측시간" : chart['PPLTN_TIME']+":00",
                "요일" : chart['DAY_NAME'],
                "예상유동인구" : chart['PREDICT'],
                "10대" : chart['PPLTN_RATE_10'].map(float),
                "20대" : chart['PPLTN_RATE_20'].map(float),
                "30대" : chart['PPLTN_RATE_30'].map(float),
                "40대" : chart['PPLTN_RATE_40'].map(float),
                "50대" : chart['PPLTN_RATE_50'].map(float),
                "60대" : chart['PPLTN_RATE_60'].map(float),
                "70대" : chart['PPLTN_RATE_70'].map(float)
            }
        )
        chart_data2.set_index("예측일자",inplace=True)
        st.dataframe(chart_data2)

        # fig = plt.figure()
        # bar_plot = plt.barh(chart_data2.iloc[:,0], chart_data2.iloc[:,[4,5]])
        # st.pyplot(fig)
        st.bar_chart(chart_data2.iloc[:,3:])
# # # 6. api - 현재 연령 분포