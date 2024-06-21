import pandas as pd
import numpy as np
import streamlit as st
import pymysql



def get_close_area(keyword):
    try:
        # mysql 연결
        conn = pymysql.connect(
        host="database-1.c3oywy0kww41.ap-northeast-2.rds.amazonaws.com", user="admin", password="rootroot",
        db="final_project", charset='utf8')
        cursor = conn.cursor()
        query_close = """
            SELECT ca.AREA_CLOSE_ENG
            FROM Close_Area ca
            JOIN Seoulcity sc ON ca.AREA_CLOSE_NM = sc.AREA_NM
            WHERE ca.ENG_NM = %s;
        """
        # 쿼리 실행
        cursor.execute(query_close, (keyword,))
        # 결과 가져오기
        result_lst = cursor.fetchall()
        result = []  # 결과 저장 리스트 초기화
        for value in result_lst:  # 각 튜플에서 첫번째 요소 추출하여 리스트에 추가
            clean_value = value['AREA_CLOSE_ENG'].strip("'")  # 작은 따옴표 제거
            result.append(clean_value)
        return result
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

st.markdown(get_close_area("Gangnam"))





