text = ("""1. 날짜 선택, 시간 선택
2. 장소 선택 -> station_select modal
3. 혼잡도 지수, 시계열 예측 모델 결과 -> congest_show page 이동
    기준: 지난 3년간의 혼잡도를 100으로 했을때 과거 대비 퍼센트 지수
4. 네이버 연관 키워드 10개, 네이버 링크 / 7days
    기준: 네이버api 연관키워드 기준
        - 전지역 공통/중복키워드 제외
        - #번출구, #호선 제외
5. 대신 어디 갈까
    기준: 선택 날짜/장소 기준 근방 5군데 중 혼잡도가 가장 낮은 곳 출력 + 과거 대비 -#%
6. 대신 언제 갈까 -> another_date page 이동""")


import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from datetime import time
import streamlit as st
import requests
import xml.etree.ElementTree as ET
import apidata as api



conn = st.connection("final_project",type="sql")
df_seoulcity = conn.query("select * from Seoulcity")
df_predict = conn.query("select * from Predict")
st.dataframe(df_predict)


city_df = df_seoulcity[['CATEGORY', 'AREA_SEARCH']]
# st.dataframe(city_df)
category = city_df['CATEGORY'].unique()
area_list = df_seoulcity['AREA_NM']
# st.text(category)


# Sql database conncet
# @st.cache
# def read_sqldata():
#     conn = st.connection('mysql', type='sql')
#     naver_df = conn.query("select * from final_project", ttl=3600)
#     return naver_df
# data = read_sqldata()


# 테스트 데이터 가져오기
# df = pd.read_csv("Data\서울시115장소명 목록_장소명수정_20240527.csv", encoding='cp949')
# city_df = df[['CATEGORY', 'AREA_SEARCH']]
# #st.dataframe(city_df)
# category = city_df['CATEGORY'].unique()
# area_list = df['AREA_NM']
#st.text(category)

# 기본 설정
# 한글폰트 설정
#print(plt.rcParams['font.family'])
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False

# 그래프 안의 한글폰트 설정
fpath = os.path.join(os.getcwd(), "Fonts\GmarketSansTTFBold.ttf") 
prop = fm.FontProperties(fname=fpath)

web_header = st.container()

# 1. 타이틀/로고 삽입



with web_header:
    st.header('YEOGIYO :sunglasses:', divider='rainbow')

apidata = api.SeoulData("강남역")
df_ppltn = apidata.seoul_ppltn()
st.dataframe(df_ppltn)

with st.sidebar:
    

    st.markdown("## How to use\n"
                "1. Select Date and Time\n"
                "2. Select location\n"
                "3. Run\n"
                "---")
    
    st.link_button("서울시 도시 데이터 바로가기", "https://data.seoul.go.kr/SeoulRtd/")
    @st.experimental_dialog("about seoul city data")
    def show_dialog():
        st.write("inside the dialog")
        if st.button("close"):
            st.rerun()

    if st.button("서울시 도시 데이터란?"):
        show_dialog()
    
    st.warning("🚧️ This app is still in beta. Please [check the version](https://github.com/) in the GitHub repo.")
    
    
    
AREA_CONGEST_LVL = '혼잡'
AREA_CONGEST_MSG = '''사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.'''
AREA_PPLTN_MIN = '23000'
AREA_PPLTN_MAX = '25000'






#new_title = '<b style="font-family:serif; color:#8675FF; font-size: 40px;">📋 서울에서 혼잡한 곳이 어디요</b>'
#st.markdown(new_title, unsafe_allow_html=True)
st.info("➡️ 1. 원하는 날짜와 시간을 선택하세요")





# 2. 날짜 & 시간 선택 객체 저장 필요
selected_date = st.date_input("When is your date", value="today")
selected_time = st.time_input("Select your time", value="now", step=3600)
#time = st.time_input("What time do you meet", value=None, step=None)
st.write("당신의 약속시간은: ", selected_date, selected_time)
#st.write("Your meeting time is:", time)

# 3. 3개 탭 생성
tab1, tab2, tab3 = st.tabs(['area1', 'area2', 'area3'])

# in tab 1)약속장소 1개 선택 
with tab1:
    st.info("➡️ 2. 아래 카테고리에서 원하는 장소 1개 선택하세요")


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
        selected_area = st.session_state.select_area['area']
        f"당신은 {st.session_state.select_area['item']} {selected_area}을 선택했습니다"


    default_area = "강남역"
    default_category = "인구밀집지역"



    # 모델 데이터 정의
    # predict_selected = 
    # predict_default =  
    

    # 파이차트 데이터 정의
    size = 0.3
    labels = '10th', '20th', '30th', '40th', '50th', '60th', '70th'
    ratio = [15, 30, 30, 10, 5, 5, 5]
    colors = ['#8675FF','#FD7289','#FF9A3E','#353E6C', '#16DBCC', '#DCFAF8', '#FFBB38']
    explode = (0, 0, 0, 0, 0, 0, 0)
    wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}



    #도넛 차트 그리기
    fig, ax = plt.subplots()
    ax.pie(ratio, colors=colors, counterclock=False, wedgeprops=dict(width=0.6),
        explode=explode, shadow=False, startangle=90, 
        autopct='%.1f%%', textprops=dict(color="w")) #,  wedgeprops=wedgeprops,autopct=(labels, ratio)


    #가운데에 텍스트 추가
    center_circle = plt.Circle((0, 0), 0.3, fc='white')
    fig.gca().add_artist(center_circle)
    ax.axis('equal') # 파이차트를 원형으로 유지
    ax.set_title("혼잡도 현황", fontproperties=prop)
    
    if select_area:
        default_area = select_area
        ax.text(0,0,df_predict['PREDICT'][0], ha='center', va='center', fontsize=32)
    # if selected_area == null:
    #     ax.text(0,0,df_predict['PREDICT'][0], ha='center', va='center', fontsize=32)
    # else:


    st.pyplot(fig)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.header(AREA_CONGEST_LVL,divider='rainbow')
    st.write(AREA_CONGEST_MSG)


    #container2.write("네이버 키워드 + 네이버 키워드 링크 연결")
    container2 = st.container(border=True)
    container2.subheader("This is Hot keyword in area")
    #to do : 텍스트 리스트 받아서 naver_keyword라는 객체에 저장, 버튼 포문 돌려서 하나씩 링크버튼 생성

    with container2:
        naver_keyword = ["keyword1", "keyword2", "keyword3", "keyword4","keyword5"]
        naver_url = ["https://www.naver.com", "https://www.naver.com", "https://www.naver.com", "https://www.naver.com","https://www.naver.com"]
        cols = st.columns(5)

        for col, keyword in zip(cols, naver_keyword):
            col.button(keyword)

        #container2.write("This will show last")


    #대신 어디 갈까

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="대신 어디 갈까?", value = "station", delta="-5%")
    
    #대신 언제 갈까
    with col2:
        st.metric(label="대신 언제 갈까?", value = "date", delta="-10%")








    with open("result/kid.jpg", "rb") as file:

        btn = st.download_button(
            label="Download data as jpg",
            data=file,
            file_name="area1.png",
            mime="image/png",
            )

















with tab2:
    st.subheader("area 2")

with tab3:
    st.subheader("area 3")



# streamlit run yeogiyo_main.py

