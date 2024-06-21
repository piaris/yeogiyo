# 🧊 오류/문제 해결
## data file 용량 이슈

### ❓ 문제 상황
### 서울시 공공데이터 수집시 json 파일 형태로 저장
* 발생한 이슈 : 서울시 공공데이터는 json 형태로 제공되는데 이를 그대로 json 파일로 저장할 경우 데이터 로드가 지연되고 및 전처리 시에 처리속도가 떨어지며 저장공간을 과도하게 차지하는 이슈가 발생함
<br><br>


---

### ❗️ 해결 방법
### 트러블 해소과정 : 저장 파일 format을 json -> parquet으로 변경

> **JSON(JavaScript Object Notation)** <br>
인간이 읽고 쓰기에 편리하며, 기계가 파싱하고 생성하기 쉬운 경량 데이터  교환 형식

> **Parquet** <br>
대규모 분산 스토리지에서 사용되는 압축된 바이너리 형식의 열 기반(column-oriented) 데이터 스토리지 파일로 대규모 데이터 셋을 처리하고 분석하는데 효율적
<br>

open API에 대한 응답으로 받은 json 파일에서 프로젝트에 필요한 column만 추출하여 parquet 파일 형태로 저장하였다.

```python
def request_congest_data(ti):
  data_df = pd.DataFrame()

  try :
    for i in range(1,116):
      url = "http://openapi.seoul.go.kr:8088/544259516c626f673332707066656a/json/citydata/1/5/POI"+f"{i}".zfill(3)
      response = requests.get(url)
      if response.status_code != 200:
        continue

      real_time_data = response.json()  # 서울시 실시간 도시데이터 전체

      if real_time_data.get("CITYDATA") == None:  # 서울시 실시간 도시 데이터 중 CITYDATA 부분이 없을 경우 넘어가기
        continue

      df = pd.DataFrame([real_time_data])
      data_df = pd.concat([data_df, df])

    buffer = BytesIO()
    table = pa.Table.from_pandas(data_df)
    pq.write_table(table, buffer)

    now_date = ti.xcom_pull(key='now_date')
    filename = f"congest_data_{now_date}.parquet"
    default_path = f'test/filename={filename}'
    # ti.xcom_push(key='df_congest', value=buffer.getvalue()

    obj = s3.Object(bucket_name, default_path)
    obj.put(Body=buffer.getvalue)
    logging.info(f'successed to upload tags_file! : {filename}')
    return {
    "successs" : "successs"
    }

  except Exception as e :
    logging.info("fail to request congest data")
    return {
      "fail" : "fail"
      }
```
<br><br>

---

### ✅ 결과
대용량 데이터(65,000건)를 json 대신 parquet 형태로 저장함으로써 각 데이터의 용량을 110 MB에서 2.8 MB로, 데이터를 읽어오는 시간을 20초에서 0.5초로 줄여 리소스를 효율적으로 활용할 수 있게 되었다.

<p align="center">
  <img src="./Gallery/img-parquet-01.png" width = 600>
</p>
<p align="center">
  <img src="./Gallery/img-parquet-02.png" width = 600>
</p><br><br>
