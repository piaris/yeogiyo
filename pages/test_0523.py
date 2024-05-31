# 국민연금 데이터 활용하여 기업의 평균 월급여, 연봉 추정하기

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import streamlit as st

plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus'] = False

class PensionData():
    
    #self 선언
    def __init__(self):
        self.df = pd.read_csv(os.path.join(filepath), encoding='cp949')
        self.pattern1 = ''
        self.pattern2 = ''
        self.pattern3 = ''
        self.preprocess()

    #전처리 함수
    def preprocess(self):
        self.df.columns = []

        df = self.df.drop([])
        df[''] = df[''].apply(self.preprocessing)
        self.df = df


    def preprocessing(self, x):
        x = re.sub(self.pattern1, '', x)
        return x
    
    def find_company(self, company_name):
        return self.df.loc[self.df[''].str.contains[], []]
    
    def compare_company(self, company_name):
        company = self.find_company(company_name)
        code = company[].iloc[0] 
        df1 = self.df.loc[self.df[] == code, []].agg([])
        return df1

    def company_info(self, company_name):
        company = self.find_company(company_name)
        return self.df.loc[company.iloc[0].name]
    
    def get_data(self):
        return self.df


## 함수 정의 완료

## 위의 데이터 한번 리딩
@st.cache
def read_pensiondata():
    data = PensionData('file.csv')
    return data

data = read_pensiondata()
company_name = st.text_input('회사명을 입력해주세요')

if data and company_name:
    output = data.find_company(company_name = company_name)
    if len(output) > 0:
        st.subheader(output.iloc[0]['사업장명'])
        info = data.company_info(company_name = company_name)
        st.markdown(
            f"""
            - `{info['주소']}`
            - 업종코드명 `{info['업종코드명']}`
            - 총 근무자 `{int(info['가입자수']):,}` 명
            - 신규 입사자 `{info['신규']:,}` 명
            - 퇴사자 `{info['상실']:,}` 명
            """
        )









    else:
        st.subheader('검색결과가 없습니다.')
