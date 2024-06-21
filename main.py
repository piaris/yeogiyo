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
import streamlit as st
import xml.etree.ElementTree as ET
import sqldata as sqldata
import requests
import apidata as apidata
from datetime import datetime, timedelta, date
import naverpage as naver
from googletrans import Translator
import time
import pyautogui

st.set_page_config(
    page_title="The most crowded area in Seoul! :sunglasses:",
    page_icon="❤️‍🔥",
    layout="centered"
)



# sql에서 데이터 불러오기
realtime_df = sqldata.sql_realtime()
naver_df = sqldata.sql_naver()
predict_df = sqldata.sql_predict()

# st.dataframe(realtime_df)
category = realtime_df['CATEGORY_ENG'].unique()
area_list = realtime_df['ENG_NM']
seoulcity_df = sqldata.sql_seoulcity()
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


# 1. 기본 설정
# 한글폰트 설정
#print(plt.rcParams['font.family'])
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False

# 그래프 안의 한글폰트 설정
fpath = os.path.join(os.getcwd(), "Fonts\GmarketSansTTFBold.ttf") 
prop = fm.FontProperties(fname=fpath)



# 2. 타이틀/로고 삽입


web_header = st.container()

with web_header:

    st.image('Gallery\YEOGIYO__logobig.png', width=600)

    st.header('The most crowded area in Seoul! :sunglasses:', divider='rainbow')



# 3. 사이드바 구성
#사이드바 로딩 캐치로 잡기
@st.cache_resource
def print_congestArea():
    return apidata.print_congestArea()

@st.cache_resource
def print_congestRoad():
    return apidata.print_congestRoad()

with st.sidebar:

    # st.image('Gallery\YEOGIYO__logobig.png', width=170)

    st.title("Welcome 👋 Yeogiyo")
    
    st.subheader(":car: The busiest place now?")
    st.write(apidata.print_congestArea())

    st.subheader(":people_holding_hands: The most congested place now?")
    st.write(apidata.print_congestRoad())

    # 경계선 & 아래 깃박스 색깔
    st.markdown("""<hr style="height:5px;border:none;color:#8675FF;background-color:#8675FF;" /> """, unsafe_allow_html=True)
    
    @st.experimental_dialog("about seoul city data")
    def show_dialog():
        st.markdown('''
    :rainbow[여기요 서울시 혼잡도 서비스는?]
                    
    서울시는 2024년 기준, 인구 960만이 살고있는 거대한 도시입니다.  
    많은 인구가 장소와 시간, 이벤트에 따라 한곳에 밀집되어 혼란과 사고를 야기할 수 있습니다.  
    :violet-background[서울 실시간 도시 데이터]의 실시간 데이터를 저장, 활용하여 한국어 사용에 한계가 있는 외국인 거주자와 관광객들의 서울 생활과 관광에 인구/교통/환경 등의 정보를 제공합니다,
    특히 서울에 오래 거주한 사람만이 알고 있을만한 **장소별 예상 혼잡도**를 제공해서 요일/시간별 일상의 유동인구를 예상하여 의사결정에 활용할 수 있도록 도움을 주고자 서비스가 기획되었습니다.

                    
    :violet[서울 실시간 도시데이터란?]

    서울 ‘주요장소’에 대해, 현재 기준 ‘분야’별 가장 최신 데이터를 융합한 데이터입니다.
                    
    :rose:주요장소: 유동인구 분석, 유관기관 대상 수요조사 등을 통해도출한 서울 주요 방문지역 115곳  
    :car:분야: 인구, 도로소통, 대중교통, 환경, 문화행사

    서울 실시간 도시데이터는 아래의 목적을 가지고 서비스를 제공하고 있습니다.
    - 일상 생활 속 시민의 의사결정 지원과 삶의 질 개선
    - 지역별 실시간 데이터 분석을 통한 지역 사업 지원 및 관광 사업활성화
    - 인구, 교통, 환경 등 각 분야 데이터 융합을 통한 서비스 확장
                    ''')
        if st.button("close"):
            st.rerun()

    if st.button("about Yeogiyo Service"):
        show_dialog()

    st.link_button("go to Seoul Realtime City data", "https://data.seoul.go.kr/SeoulRtd/")
    
    st.warning("🚧️ This app is still in beta. Please [check the version](https://github.com/piaris/yeogiyo) in the GitHub repo.")
    
# 4. 메인 서비스 3개 탭 생성
tab1, tab2, tab3 = st.tabs(['area1', 'area2', 'area3'])
with tab1:
    # 팝업 기능
    @st.experimental_dialog("select your area")
    def select_area(value):
        places=realtime_df[realtime_df['CATEGORY_ENG']==value]['ENG_NM'].values
        area = st.radio("Select one location", places)
        if st.button("select"):
            st.session_state.select_area = {"value": value, "area": area}
            st.rerun()

    # 5.1 (완) 원하는 카테고리/장소 선택
    st.info("➡️ 1. Select location from the categories below")
    st.markdown('''
                :point_right: Just select a location to get real-time information on Seoul city data.  
                (Current floating population & congestion information for the next 12 hours)
                ''')
    cols = st.columns([1,1,1,1,1])
    
    if "select_area" not in st.session_state:
        for col, value in zip(cols, category):
            with col:
                if st.button(value):
                    select_area(value)
    else:
        selected_area = st.session_state.select_area['area']
        f"You selected {selected_area} in {st.session_state.select_area['value']}."

    # 5-2 약속장소 1개 선택
    st.info("➡️ 2. Select date and time of your appointment")
    selected_date = st.date_input("When is your date", value="today")
    selected_time = st.time_input("Select your time", value="now", step=3600).hour
    st.write("Your appointment is: ", selected_date, selected_time)

    print("st.session_state.select_area", st.session_state)

    # 5.3. 화면 default값 api 호출 설정/출력
    # 1) 화면 default값 api 호출, 메시지 & 바그래프 출력
    if st.session_state.get("select_area") == None:

        default_area = "강남역"
        before_msg = apidata.get_brfore_msg(default_area)
        default_msg1 = st.text_area('Before 12 hours :balloon:', before_msg)

        focs_msg = apidata.get_focs_msg(default_area)
        default_msg2 = st.text_area('Next 12 hours', focs_msg)

        interval, datetime_interval = apidata.get_people_interval(default_area)
        # st.dataframe(interval)
        colors = ['#353E6C'] * 12 + ['#8675FF']*1 + ['#FD7289']*11

        fig_bar = plt.figure(figsize=(10,4))
        plt.bar(datetime_interval, interval, color=colors)
        plt.xlabel("Time Flow")
        plt.ylabel("People counts")
        # plt.grid()
        plt.xticks(rotation=45)
        plt.yticks()

        st.pyplot(fig_bar)

        # apidata로 24시간 과거/미래 바그래프 출력
        # interval_df = pd.DataFrame(
        #     {
        #         "유동인구" : interval[:-1],
        #         "일자/시간" : datetime_interval[:-1]
        #     }
        # )
        # st.bar_chart(interval_df, x='일자/시간', y='유동인구', color="#8675FF")

        api_default = SeoulData(default_area)
        df_ppltn = api_default.seoul_ppltn()
        # st.dataframe(df_ppltn)


        #6. 혼잡도 자세히 보기 -> congest_show페이지로 이동
        #7. (완) 이미지로 저장하기
        captured_image = None

        if st.button("Capture the result as image"):
            time.sleep(2)
            captured_image = pyautogui.screenshot()
            captured_image.save("area1_congest.png")
            st.success("Image has been captured")

        if captured_image:
            with open("area1_congest.png", "rb") as file:
                st.download_button(
                label="Save the result as image",
                data=file,
                file_name="area1_congest.png",
                mime="image/png",
                )



            # if st.button("Save the result as image"):
            #     save_path = "area1_congest.png"
            #     captured_image.save(save_path)
            #     st.success(f"이미지가 {save_path}에 저장되었습니다!")


        # 8. 네이버 키워드 출력/링크 연결
        #container2.write("네이버 키워드 + 네이버 키워드 링크 연결")
        container2 = st.container(border=True)
        container2.subheader("This is Hot keyword in area")
        #to do : 텍스트 리스트 받아서 naver_keyword라는 객체에 저장, 버튼 포문 돌려서 하나씩 링크버튼 생성

        def on_word_click(location, keywords):
            start_date, end_date = naver.set_datetime()
            url =f"https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=WEEK&orderBy=sim&startDate={start_date}&endDate={end_date}&keyword={location}{keyword}"
            return url
        #f'<a href="{url}" target="_blank">{keyword}</a>'

        with container2:
            area_temp = "강남역"
            start_date, end_date = naver.set_datetime()
            keywords_df = naver_df[naver_df['AREA_NM'] == area_temp]
            keywords = list(keywords_df['HASHTAG'])
            st.text(keywords)
            cols = st.columns(20)
            for col, keyword in zip(cols, keywords):
                naver_link = on_word_click(location=area_temp, keywords=keyword)
                #st.text(naver_link)
                col.link_button(keyword, naver_link)


    else:
        # 5.4 Predict table에서 혼잡도 가져와서 파이차트, 예상 혼잡도 출력
        # 파이차트 임시 데이터 정의
        labels = '10th', '20th', '30th', '40th', '50th', '60th', '70th'
        st.session_state["selected_area"] = seoulcity_df[seoulcity_df["ENG_NM"]==selected_area]["AREA_NM"].values[0]
        st.session_state["selected_date"] = selected_date
        st.session_state["selected_time"] = selected_time

        cond1 = predict_df["ENG_NM"]==selected_area
        cond2 = predict_df["PPLTN_DATE"]==str(selected_date)
        cond3 = predict_df["PPLTN_TIME"]==str(selected_time).zfill(2)

        selected_df = predict_df[cond1 & cond2 & cond3] 
        if select_area:
            default_area = select_area
            if len(selected_df) == 0:
                congest_result = "None"
            else:
                congest_result = selected_df['PERCENTAGE'].iloc[0]

    # print(selected_df)
        if len(selected_df) == 0:
            ratio = [1] * 7
        else:
            ratio = selected_df[selected_df.columns[selected_df.columns.str.contains("RATE_..")]].iloc[0]
        colors = [
            "#8675FF",
            "#FD7289",
            "#FF9A3E",
            "#353E6C",
            "#16DBCC",
            "#DCFAF8",
            "#FFBB38",
        ]    
        explode = (0, 0, 0, 0, 0, 0, 0)
        wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

        fig, ax = plt.subplots()
        ax.pie(ratio, colors=colors, labels=labels, counterclock=False, wedgeprops=dict(width=0.6),
            explode=explode, shadow=False, startangle=90, 
            autopct='%.1f%%') #,  wedgeprops=wedgeprops,autopct=(labels, ratio), textprops=dict(color="w")

        #가운데에 텍스트 추가
        center_circle = plt.Circle((0, 0), 0.3, fc='white')
        fig.gca().add_artist(center_circle)
        ax.axis('equal') # 파이차트를 원형으로 유지
        # ax.set_title("혼잡도 현황", fontproperties=prop)
        ax.text(0,0,congest_result, ha='center', va='center', fontsize=32)
        st.pyplot(fig)


    # 9 대신 어디 갈까

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Where should I go instead?", value = "Nonhyun Station", delta="-5%")


    
    # 10 대신 언제 갈까

    with col2:
        st.metric(label="When should I go instead?", value = "2024-06-30", delta="-10%")

        if st.button("Click for congestion details"):
            st.switch_page("pages/congest_show.py")

























with tab2:
    st.subheader("area 2")


with tab3:
    st.subheader("area 3")



# streamlit run yeogiyo_main.py

