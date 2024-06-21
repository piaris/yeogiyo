import os
import sys
import boto3
import logging
from io import StringIO
from urllib.parse import quote
from dotenv import load_dotenv

import time
import pytz
from datetime import datetime, date, timedelta
import re
import json
import pandas as pd

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures



# 검색어 가져오기
def get_keywords():
  df = pd.read_excel('data/서울시115장소명 목록_장소명수정_20240527.xlsx')
  keywords = [i for i in df['AREA_SEARCH']]
  return keywords



# 조회기간 설정
def set_datetime():
  date = datetime.now()
  start_date= (date+timedelta(days=-7)).strftime('%Y-%m-%d')
  end_date = (datetime.now()).strftime('%Y-%m-%d')
  return start_date, end_date



# 조회 url 셋팅
def set_search_url(page_num, end_date, keyword, start_date):
  search_url =f"https://section.blog.naver.com/ajax/SearchList.naver?countPerPage=7&currentPage={page_num}&endDate={end_date}&keyword={keyword}&orderBy=sim&startDate={start_date}&type=post"
  return search_url


# timpestamp
def set_kst_time(time):
  timestamp_s = time/1000
  utc_time = datetime.fromtimestamp(timestamp_s, tz=pytz.utc)
  # 한국 시간으로 변환
  kst = pytz.timezone('Asia/Seoul')
  kst_time = utc_time.astimezone(kst).strftime('%Y-%m-%d-%H:%M:%S')
  return kst_time



# 파일 저장
def save_data_to_file(data,file_path):
  pd_data = pd.DataFrame(data)
  pd_data.to_csv(file_path, index=False)
  return file_path



# s3에 크롤링 파일 업로드
def upload_file(file_name):
  start_date, end_date = set_datetime()

  load_dotenv('.env')
  bucket_name = os.getenv('bucket_name')
  s3 = boto3.client('s3')
  result = ""
  default_path = f'naver-tags-data/{result}/years={years}/months={months}/days={days}/filename={filename}'

  try:
    years = start_date.strftime("%Y")
    months = start_date.strftime("%m")
    days = start_date.strftime("%d")
    success_path = default_path.format(result="success")
    s3.upload_file(file_name, bucket_name, success_path)  # 파일 업로드
    print("파일이 성공적으로 업로드되었습니다.")
    return True
  except FileNotFoundError:
    print("로컬 파일을 찾을 수 없습니다.")
  except Exception as e:
    print(f"파일 업로드 중 오류 발생: {e}")



# dirver 및 chrome 설정
def get_driver():
  options = webdriver.ChromeOptions()
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument('headless')
  driver = webdriver.Chrome(options = options)
  return driver



# blog  data(title/url/posted_data)
def blogdata_crawling():
    keywords = get_keywords()
    blog_data = []


    # keyword별 for문
    for keyword in keywords:
        encoded_keyword = quote(keyword)
        page_num = 1
        start_date, end_date = set_datetime()

        referer = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page_num}&rangeType=WEEK&orderBy=sim&startDate={start_date}&endDate={end_date}&keyword={encoded_keyword}"
        headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
          "referer": referer
        }
        url = set_search_url(page_num,end_date,keyword,start_date)
        response = requests.get(url, headers=headers)
        response.raise_for_status()   # status_code가 200이 아닌 경우 exception 발생 시켜줌
        response_data = json.loads(response.text.strip()[6:])
        total_count = response_data['result']['totalCount']
        total_page = (total_count//7)+1
        print(f'{keyword}:total_page - {total_page}')
        max_page = 300

        if total_page >= max_page:
          total_page = 300
          print(total_page)

        for page_num in range(1,total_page+1):
            encoded_keyword = quote(keyword)
            start_date, end_date = set_datetime()
            referer = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page_num}&rangeType=WEEK&orderBy=sim&startDate={start_date}&endDate={end_date}&keyword={encoded_keyword}"
            headers = {
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
              "referer": referer
            }
            url = set_search_url(page_num,end_date,keyword,start_date)
            print(f'크롤링 시작: {keyword} - 페이지 {page_num}')
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_data = json.loads(response.text.strip()[6:])
                post_data = response_data['result']['searchList']

                # 페이지에 게시물이 없으면 종료
                if not post_data:
                    logging.info(f'{keyword} - 페이지 {page_num}에 게시물이 없습니다.')
                    break

                for post in post_data:
                    posted_date = post['addDate']
                    date = set_kst_time(posted_date)

                    if date < start_date :
                        break

                    post_title = post['noTagTitle']
                    post_url = post['postUrl']


                    # 데이터 저장
                    blog_data.append({
                        "location": keyword,
                        "title": post_title,
                        "url": post_url,
                        "posted_date": date
                    })
                logging.info(f'{keyword} - 페이지 {page_num} 크롤링 완료')
            except requests.exceptions.RequestException as e:
                logging.error(f"HTTP 요청 에러 - {keyword} - 페이지 {page_num}: {e}")
            except json.JSONDecodeError as e:
                logging.error(f"JSON 파싱 에러 - {keyword} - 페이지 {page_num}: {e}")
            except KeyError as e:
                logging.error(f"데이터 키 에러 - {keyword} - 페이지 {page_num}: {e}")
            except Exception as e:
                logging.error(f"에러 발생 - {keyword} - 페이지 {page_num}: {e}")
                continue
        print(f"{keyword} 수집 완료")

    return blog_data



# hash tag 가져오기
def tags_crawling(file_name):
    # URL 리스트 가져오기
    crawling_data = pd.read_csv(file_name)
    # 위치 리스트 가져오기
    keywords = get_keywords()
    # 제외할 단어 리스트 가져오기
    exclude_list = [exclude_word.strip() for exclude_word in pd.read_csv('data/exclude_list.csv')]

    # Chrome 드라이버 실행
    driver = get_driver()
    crawling_contents_data = []

    try:
        for keyword in keywords:
            temp = crawling_data[crawling_data['location'] == keyword]
            total_tags = 0
            for index, row in temp.iterrows():
                blog_url = str(row['url'])
                tags_text = ""  # 초기화
                try:
                    driver.get(blog_url)
                    # iframe 접근
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'mainFrame')))

                    # 태그 찾아서 가져오기
                    tags_element = driver.find_element(By.CLASS_NAME, "wrap_tag")
                    tags_text = tags_element.text

                    # 정규 표현식을 사용하여 '태그', '#', '역' 제거
                    tags_text = re.sub(r'(태그|#|역)', '', tags_text).replace(keyword, "").strip()
                    tags = [tag.strip() for tag in tags_text.split("\n") if tag.strip()]

                    # 제외할 단어가 포함된 태그가 있는지 확인
                    if any(tag in exclude_list for tag in tags):
                        continue

                    # 데이터 저장
                    if tags:
                        crawling_contents_data.append({"location": keyword, "url": blog_url, "tags": tags})
                        total_tags += len(tags)
                        print(f'{index}번째 완료: {tags} / 총 {total_tags} 개')
                        # 해시태그 개수가 200개 이상이면 다음 키워드로 넘어가기
                        if total_tags >= 200:
                            break

                except Exception as e:
                    logging.error(f"error ({index}) : {str(e)}")

    finally:
        driver.quit()  # 드라이버 종료
    return crawling_contents_data
