import os
import sys
import pandas as pd
import time
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


f = open("station.txt", 'r', encoding='utf-8')
keywords = f.readlines()
keywords_data = []

# 조회 기간 설정 : 7일(days에서 수정 가능)
# startDate=7일전 날짜, endDate=오늘 날짜
date = datetime.now()
startDate= (date+timedelta(days=-7)).strftime('%Y-%m-%d')
endDate = (datetime.now()).strftime('%Y-%m-%d')

# Chrome driver 환경설정 및 실행
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument('headless')
driver = webdriver.Chrome(options = options)

for keyword in keywords : 

    base_url = f"https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=WEEK&orderBy=sim&startDate={startDate}&endDate={endDate}&keyword={keyword}"
    driver.get(base_url)
    time.sleep(1)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    sub_keywords = []
    sub_keyword_data = soup.select_one('div.list')
    
    for i in sub_keyword_data : 
        i = i.text.strip(keyword).strip()
        if i != '' : 
            sub_keywords.append(i)
    
    
        
    keywords_data.append({"location" : keyword.rstrip('\n'), "sub_keyword" : sub_keywords, "update_date" : f'{endDate}'})
    
    
filename = f'연관검색어_{startDate}-{endDate}.xlsx'
df.to_excel(filename, index=False)