
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import time
import datetime
import requests
from pandas import json_normalize
import xml.etree.ElementTree as ET


# 실시간 서울도시API 가져와서 데이터프레임 3종류로 저장
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
