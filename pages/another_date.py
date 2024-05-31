'''
page3. 대신 어디서 볼까, 선택날짜 기준 앞7일 뒤7일 예상 혼잡도 지수 뒤로 가기

'''


import streamlit as st
import pandas as pd

button = st.button("대신 어디서 볼까")

if button:
    st.write(':blue[버튼]이 눌렀습니다 :sparkles:')