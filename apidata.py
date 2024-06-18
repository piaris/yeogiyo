
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import requests
import xml.etree.ElementTree as ET
from io import StringIO
import re
import json
from statistics import mean
from statistics import median
from concurrent.futures import ThreadPoolExecutor, as_completed
from googletrans import Translator

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


#텍스트 번역
def traslate_product(msg):
    translator = Translator()
    msg_eng = translator.translate(msg, dest='en').text
    return msg_eng

# 사이드바에서 사용할 실시간 혼잡도 순위 가져오기
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
                yield area
    except Exception as e:
        print(f"페이지의 정보를 가져올 수 없습니다. :{e}")



# '붐빔'지역의 'area_nm' 출력
def print_congestArea() :
    for area in get_congestArea_data():
        eng = traslate_product(area)
        st.text(eng)


# '붐빔'지역의 도로교통 정보(평균 주행 속력) 출력
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
            # result.append({area_nm : avg_spd})
            print(f'{area_nm}:{avg_spd} km/h')
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류: {e}")

# 여기서부터는 병렬 처리할 경우 사용되는 code
# 평균 주행 속도 구하기
def fetch_avg_spd(area_nm):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    try:
        road_url = f"https://data.seoul.go.kr/SeoulRtd/road?hotspotNm={area_nm}"
        response = requests.get(road_url, headers=header)
        response_data = json.loads(response.text)['row']
        spd_values = [float(item['SPD']) for item in response_data if 'SPD' in item]
        avg_spd = round(mean(spd_values), 1)
        return {area_nm: avg_spd}
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류 ({area_nm}): {e}")
        return {area_nm: None}
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류 ({area_nm}): {e}")
        return {area_nm: None}



# 병렬 처리
def get_congestRoad_data_parallel():
    area_list = get_congestArea_data()

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_area = {executor.submit(fetch_avg_spd, area_nm): area_nm for area_nm in area_list}
        results = []
        for future in as_completed(future_to_area):
            area_nm = future_to_area[future]
            result = future.result()
            results.append(result)
    return results



# 결과 출력
def print_congestRoad():
    results = get_congestRoad_data_parallel()
    for result in results:
        for key, value in result.items():
            eng = traslate_product(key)
            st.text(f"{eng} : {value} km/h")


#  congest MSG 가져오는 함수들 ==========================================================================================================================
# congest data 가져오기
def fetch_data(area_nm):
    url = f"https://data.seoul.go.kr/SeoulRtd/pop_congest?hotspotNm={area_nm}"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            data = response.json()[0]
            return data
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None




# 12시간 이전 메세지
def get_brfore_msg(area_nm) :
    data = fetch_data(area_nm)
    if data:
        response_data = data.get('before_instruction', '')
        focs_msg = re.sub(r'<.*?>', '', response_data)
        eng = traslate_product(focs_msg)
        return eng
    return None

# 12시간 이후 메세지
def get_focs_msg(area_nm) :
    data = fetch_data(area_nm)
    if data:
        response_data = data.get('predict_instruction', '')
        focs_msg = re.sub(r'<.*?>', '', response_data)
        eng = traslate_product(focs_msg)
        return eng
    return None



def get_people_interval(area_nm) :
    data = fetch_data(area_nm)
    if data:
        # 사람 수 데이터
        response_data = data.get('people_interval', '')
        clean_res_data = re.sub(r'[\/명]', '', response_data)
        people_interval = [value.split('~') for value in clean_res_data.split('|')]
        result_people = [int(median([float(v) for v in value])) for value in people_interval]
        # 시간 데이터
        response_time_data = data.get('time_cd', '')
        result_time = [time.strip('|') for time in response_time_data.split('|')]
        return result_people, result_time
    return None

