
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import xml.etree.ElementTree as ET
import apidata as api

# 기본설정 - 한글폰트
#print(plt.rcParams['font.family'])
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False
# 기본설정 - 디자인
# css_file = "style.css"


# 1. 모델 - 혼잡도 코멘트 + 예상 실시간 인구 (nn~nn)
# 2. 모델 - *2주간의 예측 바+선그래프
# 3. 모델 - 추후 2주간의 예측 혼잡도 지수
# 4. api - 현재 혼잡정도 + 실시간 인구 + 도로소통현황 + 코멘트 + 영상까지??
# 5. api - 12시간 예측 바그래프
# 6. api - 현재 연령 분포

area_name = st.text_input('지역명을 입력하세요',)

# 혼잡도 예측 모델 임시 데이터
congest_result = '88.8%'
# congest_style = '<b style="font-family:serif; color:#8675FF; font-size: 60px;">📋congest_result </b>'



# 4. api - 현재 혼잡정도 + 실시간 인구 + 도로소통현황 + 코멘트 + 영상까지??




data = api.SeoulData(area_name)


if data and area_name:
    df_ppltn = data.seoul_ppltn()
    df_fcst = data.seoul_fcst()
    df_traffic = data.seoul_traffic()

    col1, col2 = st.columns([0.3,1])
    with col1:
        
        st.subheader(congest_result)

    with col2:
        st.write(area_name,'은 현재' , df_ppltn['AREA_CONGEST_LVL'][0], '입니다.')
        st.write('예상 실시간 인구는', df_ppltn['AREA_PPLTN_MIN'][0], '~',df_ppltn['AREA_PPLTN_MAX'][0], '입니다')
        st.write('지난 (분석기간)에 비해', congest_result, '혼잡합니다.')
        
    st.divider()

# else:
#     st.subheader('검색결과가 없습니다')



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

if data and area_name:

    with st.container():
        st.subheader(area_name, '의 2주간의 예측 인구 그래프')

        chart_data = pd.DataFrame(
            {

            "예측시간" : list(df_fcst['FCST_TIME']),
            "유동인구(최소)" : df_fcst['FCST_PPLTN_MIN'],
            "유동인구(최대)" : df_fcst['FCST_PPLTN_MAX']
            }
        )

        st.bar_chart(chart_data, x="예측시간", y=["유동인구(최소)", "유동인구(최대)"], color=['#8675FF','#FD7289'])



# # 6. api - 현재 연령 분포



