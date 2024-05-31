import streamlit as st
import pandas as pd
from streamlit_modal import Modal
from datetime import datetime as dt
import datetime




# multi-select

options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"])

st.write("You selected:", options)

# popup - modal
modal = Modal(
    "Demo popup",
    key = "demo-modal",

    #optional
    padding = 20,
    max_width=744
    )

open_popup = st.button("Select Location")

if open_popup:
    modal.open()

if modal.is_open():
    with modal.container():
        st.write("text goes here")

        st.write("some fancy text")
        value = st.checkbox("check me")
        st.write(f"checkbox checked {value}")



@st.experimental_dialog("Select your Location")
def vote(item):
    area = st.radio('select your area',
                ['강남역',
                '논현역',
                '서초역'])
    
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "area": area}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("관광특구"):
        vote("관광특구")
    if st.button("문화유산"):
        vote("문화유산")
    if st.button("인구밀집지역"):
        vote("인구밀집지역")
    if st.button("발달상권"):
        vote("발달상권")
    if st.button("공원"):
        vote("공원")
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['area']}"

#버튼 생성
button = st.button("버튼을 눌러보세요")

if button:
    st.write(':blue[버튼]이 눌렀습니다 :sparkles:')

#파일 다운로드 버튼
#샘플 데이터 생성

dataframe = pd.DataFrame({
    'first column': [1,2,3,4],
    'second column': [10,20,30,40],
})

# 다운로드 버튼 연결
st.download_button(
    label='CSV로 다운로드',
    data= dataframe.to_csv(),
    file_name='sample.csv',
    mime='text/csv'
)

# 체크박스
agree = st.checkbox("동의 하십니까")

if agree:
    st.write("동의 해주셔서 감사합니다 :100:")

