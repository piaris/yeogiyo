## ⭐ Yeogiyo 서울시 혼잡도 공유서비스 ⭐

![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/YEOGIYO__logobig.png)

- 배포 url : https://yeogiyo.streamlit.app/

<br>

안녕하세요! 우리 프로젝트 깃에 오신것을 환영합니다.🎈
'여기요' 웹서비스는 **2024년 Playdata final progect** 로 진행되며 서울시 도시 데이터를 활용하여 장소별 유동인구와 혼잡도 예측서비스 제공합니다.

## 😊 프로젝트 스토리텔링 🛩️

서울시는 2024년 기준, 인구 960만이 살고있는 거대한 도시입니다.
많은 인구가 장소와 시간, 이벤트에 따라 한곳에 밀집되어 혼란과 사고를 야기할 수 있습니다.
특히 서울을 처음 오는 외국인과 관광객의 경우 서울의 규모를 잘 모르면 혼잡함에 크게 당황하여 큰 스트레스가 될 수 있습니다.
'여기요' 웹서비스는 한국어를 몰라 **서울 실시간 도시 데이터** 공공 서비스 사용에 한계를 가지는 외국인들을 위해 서울의 주요 115개 장소별 과거/현재 혼잡도(유동인구/교통상황) 및 분석 인사이트를 제공하고 미래 2주간의 예측정보를 제공하여 서울 생활과 관광에 편리함을 제공합니다.
또한 장소별 네이버 검색 키워드를 제공하여 장소가 가지는 특징과 트렌드 정보를 함께 제공합니다.

<br>

**과거/현재 기반 데이터,** 서울시 제공 실시간 도시 데이터 API 활용
**예측 기반 추천 데이터,** 머신러닝(랜던포레스트) 기반 혼잡도 예측 모델

## 👍 팀원 구성 및 역활

<div align="center">

| **조은별** | **김서윤** | **유승민** |
| :------: |  :------: | :------: |
| [<img src="https://avatars.githubusercontent.com/u/141891949?v=4" height=150 width=150> <br/> @piaris](https://github.com/piaris) | [<img src="https://avatars.githubusercontent.com/u/156580003?v=4" height=150 width=150> <br/> @kimppu](https://github.com/kimppu) | [<img src="https://avatars.githubusercontent.com/u/68213803?v=4" height=150 width=150> <br/> @YUSEONGMIN](https://github.com/YUSEONGMIN) |

**조은별(팀장)** : **데이터분석** + **서비스 기획** 화면구현, 머신러닝
**김서윤** : **백엔드** + **데이터엔지니어링** 머신러닝 보조
**유성민** : **데이터 분석** + **머신러닝** 데이터엔지니어링 보조

## 2. 📉 데이터 출처

[서울시 실시간 도시데이터(주요 50 장소)(OPEN API)](https://data.seoul.go.kr/dataList/OA-21285/F/1/datasetView.do)

## 3. 개발 환경

**프론트/백엔드** : Pandas, Streamlit, matplotlib
**데이터분석** : Pandas, Randomforest, LSTM
**데이터엔지니어링** : Mysql, Pandas, Selenium, Requests, Airflow
**클라우드** : AWS(S3, EC2, RDS, Lambda)
**형상관리** : Git, Github
**커뮤니케이션**: Slack

## 3. 채택한 기술스택과 브랜치 전략

[🙋‍♂️ 스택 사용 스토리](READSTACK.md)

## 4. 🧊 오류/문제 해결

[🙋‍♂️ 문제 해결 스토리](READERROR.md)

## 서비스 파이프라인

![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/data_0618.png)

## 📶 데이터파이프라인

![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/data_0618.png)

## 📂 데이터 ERD

![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/erd_0618.png)

## 개발 기간 : 2024-04-29 ~ 2024-06-21

## 🌎 기대효과

1. batch성 데이터 스크래핑 및 실시간 데이터 적재(Airflow) 기술 확보
2. 데이터파이프라인 구축 기술 확보
3. 데이터 분석, 머신러닝, 서비스 활용
4. 파이썬으로 반응형 웹서비스 배포 기술 활용
5. 네이버 실시간 크롤링 기술 획득과 활용
6. 서울시 생활과 관광을 위한 혼잡도 기반 웹(공공데이터 활용사례 출품 예정)

## 화면 소개

## Service Flow Chart

![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/service_flow_0618.png)

### [메인화면]

### [혼잡도 화면]
