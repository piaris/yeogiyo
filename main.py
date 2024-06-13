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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from datetime import time
import streamlit as st
import xml.etree.ElementTree as ET
import sqldata as sqldata
from io import StringIO
import json
import requests
from statistics import mean

# sql에서 데이터 불러오기
realtime_df = sqldata.sql_realtime()
# st.dataframe(realtime_df)
category = realtime_df['CATEGORY'].unique()
area_list = realtime_df['AREA_NM']
# st.text(category)


# api 실시간 데이터 가져오기
# 실시간 서울도시API 가져와서 데이터프레임 3종류로 저장
@st.cache_resource
class SeoulData():
    def __init__(self, area_input):
        self.url = "http://openapi.seoul.go.kr:8088/544259516c626f673332707066656a/xml/citydata/1/5/" + area_input
#         self.data_ppltn = './/LIVE_PPLTN_STTS'
#         self.data_road = './/ROAD_TRAFFIC_STTS'
#         self.data_fcst = './/FCST_PPLTN'
        res = requests.get(self.url)
        res_content = res.content
        self.root = ET.fromstring(res_content)
        
    def seoul_ppltn(self):
        live_ppltn_stts = self.root.find('.//LIVE_PPLTN_STTS')
        data01 = {
            'AREA_NM': self.root.find('.//AREA_NM').text,
            'AREA_CD': self.root.find('.//AREA_CD').text,
            'AREA_CONGEST_LVL': live_ppltn_stts.find('.//AREA_CONGEST_LVL').text,
            'AREA_CONGEST_MSG': live_ppltn_stts.find('.//AREA_CONGEST_MSG').text,
            'AREA_PPLTN_MIN': int(live_ppltn_stts.find('.//AREA_PPLTN_MIN').text),
            'AREA_PPLTN_MAX': int(live_ppltn_stts.find('.//AREA_PPLTN_MAX').text),
            'MALE_PPLTN_RATE': float(live_ppltn_stts.find('.//MALE_PPLTN_RATE').text),
            'FEMALE_PPLTN_RATE': float(live_ppltn_stts.find('.//FEMALE_PPLTN_RATE').text),
            'PPLTN_RATE_0': float(live_ppltn_stts.find('.//PPLTN_RATE_0').text),
            'PPLTN_RATE_10': float(live_ppltn_stts.find('.//PPLTN_RATE_10').text),
            'PPLTN_RATE_20': float(live_ppltn_stts.find('.//PPLTN_RATE_20').text),
            'PPLTN_RATE_30': float(live_ppltn_stts.find('.//PPLTN_RATE_30').text),
            'PPLTN_RATE_40': float(live_ppltn_stts.find('.//PPLTN_RATE_40').text),
            'PPLTN_RATE_50': float(live_ppltn_stts.find('.//PPLTN_RATE_50').text),
            'PPLTN_RATE_60': float(live_ppltn_stts.find('.//PPLTN_RATE_60').text),
            'PPLTN_RATE_70': float(live_ppltn_stts.find('.//PPLTN_RATE_70').text),
            'RESNT_PPLTN_RATE': float(live_ppltn_stts.find('.//RESNT_PPLTN_RATE').text),
            'NON_RESNT_PPLTN_RATE': float(live_ppltn_stts.find('.//NON_RESNT_PPLTN_RATE').text),
            'REPLACE_YN': live_ppltn_stts.find('.//REPLACE_YN').text,
            'PPLTN_TIME': live_ppltn_stts.find('.//PPLTN_TIME').text,
        }
        df_PPLTN = pd.DataFrame([data01])
        return df_PPLTN
    
    def seoul_traffic(self):
        road_traffic_stts = self.root.find('.//ROAD_TRAFFIC_STTS')
        data02 = {
            'AREA_NM': self.root.find('.//AREA_NM').text,
            'AREA_CD': self.root.find('.//AREA_CD').text,
            'ROAD_TRAFFIC_IDX': road_traffic_stts.find('.//ROAD_TRAFFIC_IDX').text,
            'ROAD_MSG': road_traffic_stts.find('.//ROAD_MSG').text,
            'ROAD_TRAFFIC_SPD': int(road_traffic_stts.find('.//ROAD_TRAFFIC_SPD').text),
            'ROAD_TRFFIC_TIME': road_traffic_stts.find('.//ROAD_TRFFIC_TIME').text,
        }
        df_TRAFFIC = pd.DataFrame([data02])
        return df_TRAFFIC
    
    def seoul_fcst(self):
        live_ppltn_stts = self.root.find('.//LIVE_PPLTN_STTS')
        fcst_ppltn_list = live_ppltn_stts.findall('.//FCST_PPLTN')

        fcst_data = []
        for fcst in fcst_ppltn_list:
            fcst_entry = {
                'FCST_TIME': fcst.find('.//FCST_TIME').text,
                'FCST_CONGEST_LVL': fcst.find('.//FCST_CONGEST_LVL').text,
                'FCST_PPLTN_MIN': int(fcst.find('.//FCST_PPLTN_MIN').text),
                'FCST_PPLTN_MAX': int(fcst.find('.//FCST_PPLTN_MAX').text),
            }
            fcst_data.append(fcst_entry)

        df_fcst = pd.DataFrame(fcst_data)
        return df_fcst



# 사이드바에서 사용할 실시간 혼잡도 순위 가져오기
@st.cache_data
def get_congestArea_data() :
    url = "https://data.seoul.go.kr/SeoulRtd/getCategoryList?page=1&category=%EC%A0%84%EC%B2%B4%EB%B3%B4%EA%B8%B0&count=15&sort=true"
    header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "referer" : "https://data.seoul.go.kr/SeoulRtd/list"
    }

    congest_area = []

    try :
        response = requests.get(url, headers=header)
        response_data = json.loads(response.text)
        congest_data=response_data['row'][:5]
        for data in congest_data:
            congest_lv = data['area_congest_lvl']
            area = data['area_nm']
            if congest_lv == '붐빔' :
                congest_area.append(area)
    except Exception as e:
        print(e)

    return congest_area

@st.cache_data
def get_congestRoad_data():
    area_list = get_congestArea_data()
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    result = []
    try:
        for area_nm in area_list:
            road_url = f"https://data.seoul.go.kr/SeoulRtd/road?hotspotNm={area_nm}"
            response = requests.get(road_url, headers=header)
            response_data = json.loads(response.text)['row']
            spd_values = [float(item['SPD']) for item in response_data if 'SPD' in item]
            avg_spd = round(mean(spd_values), 1)
            result.append({area_nm: avg_spd})
        return result
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류: {e}")

# 1. 기본 설정
# 한글폰트 설정
#print(plt.rcParams['font.family'])
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False

# 그래프 안의 한글폰트 설정
fpath = os.path.join(os.getcwd(), "Fonts\GmarketSansTTFBold.ttf") 
prop = fm.FontProperties(fname=fpath)

# 2. 화면 default값 설정

apidata = SeoulData("강남역")
df_ppltn = apidata.seoul_ppltn()
# st.dataframe(df_ppltn)

# 3. 타이틀/로고 삽입
web_header = st.container()

with web_header:

    st.image('Gallery\YEOGIYO__logobig.png', width=200)

    st.header('서울에서 혼잡한 곳은 어디요! :sunglasses:', divider='rainbow')


# 4. 사이드바 구성

with st.sidebar:

    # st.image('Gallery\YEOGIYO__logobig.png', width=170)

    st.title("Welcome 👋 Yeogiyo")
    
    st.subheader("지금 가장 바쁜 곳은?")
    st.text(get_congestArea_data())

    st.subheader("지금 가장 막히는 곳은?")
    st.text(get_congestRoad_data())

    # 경계선 & 아래 깃박스 색깔
    st.markdown("""<hr style="height:5px;border:none;color:#8675FF;background-color:#8675FF;" /> """, unsafe_allow_html=True)

    st.info(
        """## How to use\n"
                "1. Select Date and Time\n"
                "2. Select location\n"
                "3. Run\n"
                "---"
        """
        )
    

    st.link_button("서울시 도시 데이터 바로가기", "https://data.seoul.go.kr/SeoulRtd/")
    @st.experimental_dialog("about seoul city data")
    def show_dialog():
        st.write("inside the dialog")
        if st.button("close"):
            st.rerun()

    if st.button("서울시 도시 데이터란?"):
        show_dialog()
    
    st.warning("🚧️ This app is still in beta. Please [check the version](https://github.com/piaris/yeogiyo) in the GitHub repo.")
    
    
    
AREA_CONGEST_LVL = '혼잡'
AREA_CONGEST_MSG = '''사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.'''
AREA_PPLTN_MIN = '23000'
AREA_PPLTN_MAX = '25000'


# 5. 메인 서비스 3개 탭 생성
tab1, tab2, tab3 = st.tabs(['area1', 'area2', 'area3'])
with tab1:
    # 5-1 default 결과값 설정
    default_area = "강남역"
    default_category = "인구밀집지역"

    # 5-2 약속장소 1개 선택
    st.info("➡️ 1. 아래 카테고리에서 원하는 장소 1개 선택하세요")
    # 팝업 기능
    @st.experimental_dialog("select your area")
    def select_area(item):
        places=realtime_df[realtime_df['CATEGORY']==item]['AREA_SEARCH'].values
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



    # 5-2 약속장소 1개 선택
    st.info("➡️ 2. 원하는 날짜와 시간을 선택하세요")
    selected_date = st.date_input("When is your date", value="today")
    selected_time = st.time_input("Select your time", value="now", step=3600)
    st.write("당신의 약속시간은: ", selected_date, selected_time)


    # 파이차트 임시 데이터 정의
    size = 0.3
    labels = ['10대', '20대', '30대', '40대', '50대', '60대', '70대']
    ratio = [15, 30, 30, 10, 5, 5, 5]
    colors = ['#8675FF','#FD7289','#FF9A3E','#353E6C', '#16DBCC', '#DCFAF8', '#FFBB38']
    explode = (0, 0, 0, 0, 0, 0, 0)
    wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

    # 5-3  파이차트 그리기
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        if st.button("혼잡도 자세히 보기"):
            st.switch_page("pages/congest_show.py")

    #도넛 차트 그리기
    fig, ax = plt.subplots()
    ax.pie(ratio, colors=colors, counterclock=False, wedgeprops=dict(width=0.6),
        explode=explode, shadow=False, startangle=90, 
        autopct='%.1f%%', textprops=dict(color="w"), labels=labels, labeldistance=2) #,  wedgeprops=wedgeprops,autopct=(labels, ratio)

    #가운데에 텍스트 추가
    center_circle = plt.Circle((0, 0), 0.3, fc='white')
    fig.gca().add_artist(center_circle)
    ax.axis('equal') # 파이차트를 원형으로 유지
    ax.set_title("혼잡도 현황", fontproperties=prop)
    
    
    if select_area:
        default_area = select_area
        predict_df = sqldata.sql_predict()
        congest_result = predict_df['PREDICT'][0]
        ax.text(0,0,congest_result, ha='center', va='center', fontsize=32)
        
        
    # if selected_area == null:
    #     ax.text(0,0,df_predict['PREDICT'][0], ha='center', va='center', fontsize=32)
    # else:

    st.pyplot(fig)

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

