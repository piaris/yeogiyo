from io import StringIO
import json
import requests
from statistics import mean

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