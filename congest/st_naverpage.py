import streamlit as st
from datetime import datetime, timedelta, date
from naver_crawling import set_datetime

def on_word_click(loation, keyword):
    start_date, end_date = set_datetime()
    url =f"https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=WEEK&orderBy=sim&startDate={start_date}&endDate={end_date}&keyword={location}{keyword}"
    return f'<a href="{url}" target="_blank">{keyword}</a>'

# 클릭 가능한 링크 표시
# '강남역', '맛집' 부분에 parmeter 받아온 거 들어가게 넣어주면 됨
st.markdown(on_word_click('강남역','맛집'), unsafe_allow_html=True)