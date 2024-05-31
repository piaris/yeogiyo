'''
page2. 혼잡도 결과, 뒤로 가기

'''

import os
import warnings
import pandas as pd
import numpy as np
import streamlit as st


button = st.button("혼잡도 분석결과")

if button:
    st.write(':blue[버튼]이 눌렀습니다 :sparkles:')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)