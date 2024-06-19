<div align="center">

![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/YEOGIYO__logobig.png)

## ⭐ Yeogiyo ⭐

안녕하세요! 우리 프로젝트 깃에 오신것을 환영합니다.🎈 <br>
'여기요' 웹서비스는 **2024년 Playdata final progect** 로 진행되며 서울시 도시 데이터를 활용하여 장소별 유동인구와 혼잡도 예측서비스 제공합니다.

## 😊 프로젝트 스토리텔링 🛩️

서울시는 2024년 기준, 인구 960만이 살고있는 거대한 도시입니다. <br>
많은 인구가 장소와 시간, 이벤트에 따라 한곳에 밀집되어 혼란과 사고를 야기할 수 있습니다. <br>
특히 서울을 처음 오는 외국인과 관광객의 경우 서울의 규모를 잘 모르면 혼잡함에 크게 당황하여 큰 스트레스가 될 수 있습니다. <br>
'여기요' 웹서비스는 한국어를 몰라 **서울 실시간 도시 데이터** 공공 서비스 사용에 한계를 가지는 외국인들을 위해 서울의 주요 115개 장소별 과거/현재 혼잡도(유동인구/교통상황) 및 분석 인사이트를 제공하고 미래 2주간의 예측정보를 제공하여 서울 생활과 관광에 편리함을 제공합니다.
또한 장소별 네이버 검색 키워드를 제공하여 장소가 가지는 특징과 트렌드 정보를 함께 제공합니다. <br>
<br>
**과거/현재 기반 데이터,** 서울시 제공 실시간 도시 데이터 API 활용<br>
**예측 기반 추천 데이터,** 머신러닝(랜던포레스트) 기반 혼잡도 예측 모델

## 👍 팀원별 역할

**조은별(팀장)** : **데이터분석** + **서비스 기획** 화면구현, 머신러닝 <br>
**김서윤** : **데이터엔지니어링** 머신러닝 보조 <br>
**유성민** : **데이터 분석** + **머신러닝** 데이터엔지니어링 보조 <br>

## 📉 데이터 출처

- [서울시 실시간 도시데이터(주요 50 장소)(OPEN API)](https://data.seoul.go.kr/dataList/OA-21285/F/1/datasetView.do)

## 🧊 기술스택

[🙋‍♂️ 스택 사용 스토리](READSTACK.md)

```bash
**프론트/백엔드** : Pandas, Streamlit, matplotlib
**데이터분석** : Pandas, Randomforest, LSTM
**데이터엔지니어링** : Mysql, Pandas, Selenium, Requests, Airflow
**클라우드** : AWS(S3, EC2, RDS, Lambda)
**형상관리** : Git, Github
**커뮤니케이션**: Slack
```

## 🧊 오류/문제 해결

[🙋‍♂️ 문제 해결 스토리](READERROR.md)

## 📶 데이터파이프라인
![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/data_pipeline_architecture.png)

## 📶 서비스 플로
![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/service_flow_0618.png)

## 📂 데이터 ERD
![ICON](https://github.com/piaris/yeogiyo/blob/main/Gallery/erd_0618.png)

## 🌎 기대효과

1. batch성 데이터 스크래핑 및 실시간 데이터 적재(Airflow) 기술 확보
2. 데이터파이프라인 구축 기술 확보
3. 데이터 분석, 머신러닝, 서비스 활용
4. 파이썬으로 반응형 웹서비스 배포 기술 활용
5. 네이버 실시간 크롤링 기술 획득과 활용
6. 서울시 생활과 관광을 위한 혼잡도 기반 웹(공공데이터 활용사례 출품 예정)
