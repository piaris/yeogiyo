# 🧊 오류/문제 해결
## 모델링 이슈

### ❓ 문제 상황
### 예측 성능이 좋지 않음
* 발생한 이슈 : `Prophet` 모델을 쓴 결과가 좋지 않았음
<br><br>

---

### ❗️ 해결 방법
### 트러블 해소과정 : 데이터 정제

> **Grouping**
<br>  
데이터가 5분 단위로 수집되어 시간 단위의 예측을 하는데 큰 효과를 미치지 않음
<br>

5분 단위로 예측하기엔 필요성과 성능이 떨어져 시간별 그룹화를 통해 데이터를 줄였음 (80,000건 -> 450건)

```py
# 그룹화
df["ds"] = pd.to_datetime(df["ds"]).dt.strftime("%Y-%m-%d %H:00:00")
df.groupby("ds", as_index=False).mean()
```

```py
# Prophet
df["ds"] = pd.to_datetime(df["ds"]).dt.strftime("%Y-%m-%d %H:00:00")
m = Prophet()
m.fit(df.groupby("ds", as_index=False).mean()[:-8])

future = m.make_future_dataframe(periods=8, freq="H")
forecast = m.predict(future)
forecast.tail(8).loc[:, ["ds", "yhat"]]
y_pred = forecast.tail(8)["yhat"].values
y_true = df.groupby("ds", as_index=False).mean().tail(8)["y"].values

# RMSE
mean_squared_error(y_true, y_pred) ** (1 / 2)
```

<br><br>

---

### ✅ 결과

강남역의 경우, RMSE 값이 26943 나왔고, 다른 모델과 비교하기로 함

### 📋 모델 비교

비교 모델은 `RandomForest`, `LSTM`을 이용  

```py
# RandomForest
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols = list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    for i in range(0, n_out):
        cols.append(df.shift(-i))
    agg = pd.concat(cols, axis=1)
    if dropnan:
        agg.dropna(inplace=True)
    return agg.values

def train_test_split(data, n_test):
    return data[:-n_test, :], data[-n_test:, :]
  
def random_forest_forecast(train, testX):
    train = np.asarray(train)
    trainX, trainy = train[:, :-1], train[:, -1]
    model = RandomForestRegressor(n_estimators=1000)
    model.fit(trainX, trainy)
    yhat = model.predict([testX])
    return yhat[0]

def walk_forward_validation(data, n_test):
    predictions = list()
    train, test = train_test_split(data, n_test)
    history = [x for x in train]
    for i in range(len(test)):
        testX, testy = test[i, :-1], test[i, -1]
        yhat = random_forest_forecast(history, testX)
        predictions.append(yhat)
        history.append(test[i])
        print(">expected=%.1f, predicted=%.1f" % (testy, yhat))

    error = mean_squared_error(test[:, -1], predictions) ** (1 / 2)
    return error, test[:, -1], predictions
```

`RandomForest`의 RMSE: 13035  
`LSTM`의 RMSE: 14624  

가장 오차가 적은 RandomForest를 이용