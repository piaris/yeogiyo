import streamlit as st
from datetime import datetime, timedelta, date

# 조회기간 설정
def set_datetime():
    date = datetime.now()
    start_date= (date+timedelta(days=-7)).strftime('%Y-%m-%d')
    end_date = (datetime.now()).strftime('%Y-%m-%d')
    return start_date, end_date





