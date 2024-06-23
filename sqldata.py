import pandas as pd
import numpy as np
import streamlit as st

def sql_realtime():
    conn = st.connection("final_project",type="sql") 
    data = conn.query("select * from Seoulcity")
    return data  

@st.cache_data
def sql_predict():
    conn = st.connection("final_project",type="sql")

    data = conn.query("select * from Predict")
    return data

@st.cache_data
def sql_naver():
    conn = st.connection("final_project",type="sql")
    data = conn.query("select * from Naver")
    return data

@st.cache_data
def sql_forecast():
    conn = st.connection("final_project",type="sql")
    data = conn.query("select * from Forecast")
    return data

@st.cache_data
def sql_seoulcity():
    conn = st.connection("final_project",type="sql")
    data = conn.query("select * from Seoulcity")
    return data