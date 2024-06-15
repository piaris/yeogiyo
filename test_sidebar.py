
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import requests
import xml.etree.ElementTree as ET
import apidata as api



st.markdown("## How to use\n"
            "1. Select Date and Time\n"
            "2. Select location\n"
            "3. Run\n"
            "---")

st.link_button("서울시 도시 데이터 바로가기", "https://data.seoul.go.kr/SeoulRtd/")
@st.experimental_dialog("about seoul city data")
def show_dialog():
    st.write("inside the dialog")
    if st.button("close"):
        st.rerun()

if st.button("서울시 도시 데이터란?"):
    show_dialog()

st.warning("🚧️ This app is still in beta. Please [check the version](https://github.com/) in the GitHub repo.")