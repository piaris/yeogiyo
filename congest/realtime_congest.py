from io import StringIO
import json
import requests
from statistics import mean
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed


# '붐빔' 지역 area_nm 가져오기
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
        st.error(f"페이지의 정보를 가져올 수 없습니다.: {e}")



# '붐빔'지역의 'area_nm' 출력
def print_congestArea() :
    for area in get_congestArea_data():
            st.write(area)



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
        st.error(f"HTTP 요청 오류: {e}")
    except json.JSONDecodeError as e:
        st.error(f"JSON 디코딩 오류: {e}")



# 추가 ========================================================================================================================== 
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
            st.write(f"{key} : {value} km/h")
