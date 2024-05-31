
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
from pandas import json_normalize

import streamlit as st




# 테스트 데이터 가져오기
df = pd.read_csv("data\서울시115장소명 목록_장소명수정_20240527.csv", encoding='cp949')
area_list = df['AREA_NM']

@st.experimental_dialog("Select your area")
def ppltn_area():
    ppltn = st.radio("Select one area:", area_list)
    if st.button('select'):
        st.session_state.ppltn_area = {"ppltn": ppltn}
        st.rerun()

if "ppltn_area" not in st.session_state:
    if st.button("실시간 혼잡도 보기"):
        ppltn_area()

else:
    f"You selected {st.session_state.ppltn_area['ppltn']}"
    input_area = st.session_state.ppltn_area['ppltn']

# 서울시 도시 데이터 실시간 데이터 가져오기
url = "http://openapi.seoul.go.kr:8088/544259516c626f673332707066656a/json/citydata_ppltn/1/5/" + input_area
res = requests.get(url)
data = res.json()

# 인구 데이터 부분을 데이터프레임으로 변환
ppltn_data = json_normalize(data['SeoulRtd.citydata_ppltn'])

# # 예측 인구 데이터 부분을 데이터프레임으로 변환
fcst_data = json_normalize(data['SeoulRtd.citydata_ppltn'][0]['FCST_PPLTN'])


st.dataframe(ppltn_data)
st.dataframe(fcst_data)
st.divider()
st.text(ppltn_data["AREA_CONGEST_MSG"])

with st.container:
    with st.expander(":rainbow[*장소를 선택하세요*]"):
        # for i in category:
        #     st.selectbox(f'{i}', df[df['CATEGORY']==i]['AREA_NM'].values)
        selected_place = None
# selected_place1 = st.selectbox('Select a place from Category 1', [''] + category1, key='Category 1')

        selected1 = st.selectbox('1. 관광특구', [''] + df[df['CATEGORY']=='관광특구']['AREA_NM'].values)
        selected2 = st.selectbox('2. 발달상권', [''] + df[df['CATEGORY']=='발달상권']['AREA_NM'].values)
        selected3 = st.selectbox('3. 인구밀집지역', [''] + df[df['CATEGORY']=='인구밀집지역']['AREA_NM'].values)
        selected4 = st.selectbox('4. 공원', [''] + df[df['CATEGORY']=='공원']['AREA_NM'].values)
        selected5 = st.selectbox('5. 공원.문화유산', [''] + df[df['CATEGORY']=='고궁·문화유산']['AREA_NM'].values)

        selected_places = [selected1,selected2,selected3,selected4,selected5]

        for place in selected_places:
            if place:
                selected_place = place
                break


        if selected_place:
            st.write("You selected: ", selected_place)
        else:
            st.write('Please select a place')