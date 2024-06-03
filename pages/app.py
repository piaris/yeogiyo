import os
import warnings
import streamlit as st
import pandas as pd
import numpy as np

# 테스트 데이터 가져오기
df = pd.read_csv("Data\서울시115장소명 목록_장소명수정_20240527.csv", encoding='cp949')
city_df = df[['CATEGORY', 'AREA_SEARCH']]
#st.dataframe(city_df)
category = city_df['CATEGORY'].unique()
#st.text(category)
#category_temp = ['관광특구', '고궁·문화유산', '인구밀집지역', '발달상권', '공원']


#카테고리 버튼 생성
# col1, col2, col3, col4, col5 = st.columns(5)
# with col1:
#     if button('')

# modal = Modal("장소 선택",
#     key="demo-moral", 
#     # Optional
#     padding=20,    # default value
#     max_width=744  # default value
#     )
# cols = st.columns(5)

# for col, value in zip(cols, category):
#     places=city_df[city_df['CATEGORY']=='category']['AREA_SEARCH'].values
#     with col:
#         open_modal=st.button(value)
#         if open_modal:
#             with modal.container():
#                 st.checkbox(places)

# for col in st.columns(5):
#     with col:
#         open_modal= st.button(label='button')
#         if open_modal:
#             with modal.container():
#                 st.checkbox(city_df.columns)





@st.experimental_dialog("select your area")
def select_area(item):
    places=city_df[city_df['CATEGORY']==item]['AREA_SEARCH'].values
    area = st.radio("한 지역을 선택하세요", places)
    if st.button("select"):
        st.session_state.select_area = {"item": item, "area": area}
        st.rerun()

cols = st.columns(5)

if "select_area" not in st.session_state:
    for col, value in zip(cols, category):
        with col:
            if st.button(value):
                select_area(value)

else:
    f"당신은 {st.session_state.select_area['item']} {st.session_state.select_area['area']}을 선택했습니다"