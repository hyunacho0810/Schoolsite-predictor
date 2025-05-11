#RandomForestRegressor>minmax scale, resampling, 상권
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# 파일 첨부
uploaded_file = "/content/학습 resampling 2.csv"  # 파일 경로에 맞게 수정하세요.

# 데이터 불러오기
data = pd.read_csv(uploaded_file, encoding='cp1252')

# 데이터를 나누기 위해 train, valid, test 데이터셋으로 분할
train, test = train_test_split(data, test_size=0.2, random_state=42)
train, valid = train_test_split(train, test_size=0.2, random_state=42)

# 나이대를 묶은 새로운 특성 생성
def create_age_groups(data):
    data["baby"] = data["under10"] + data["10s"]
    data["청년"] = data["20s"] + data["30s"]
    data["장년층"] = data["40s"] + data["50s"] + data["60s"]
    data["노년층"] = data["70s"] + data["80s"] + data["90s"]
    return data

train = create_age_groups(train)
valid = create_age_groups(valid)
test = create_age_groups(test)

# y 값을 제외한 항목에 대해 MinMax 스케일링 진행
scaler = MinMaxScaler()
columns_to_scale = ['size', 'latitude', 'longitude', 'Population_woman', 'Population_man',
                    'under10', '10s', '20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s',
                    'transit_count', 'number of type0', 'number of type1', 'number of type2',
                    'number of type3', 'total', 'Store_count']
train[columns_to_scale] = scaler.fit_transform(train[columns_to_scale])
valid[columns_to_scale] = scaler.transform(valid[columns_to_scale])
test[columns_to_scale] = scaler.transform(test[columns_to_scale])

# X와 y 데이터를 분리
X_train = train.drop(columns=['user'])
y_train = train['user']
X_valid = valid.drop(columns=['user'])
y_valid = valid['user']
X_test = test.drop(columns=['user'])
y_test = test['user']

# RandomForestRegressor 모델 초기화 및 학습
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# 검증 데이터로 성능 평가
valid_score = model.score(X_valid, y_valid)
print(f"Validation R^2 score: {valid_score}")

# 테스트 데이터로 성능 평가
test_score = model.score(X_test, y_test)
print(f"Test R^2 score: {test_score}")

# 검증 데이터 예측 및 RMSE 계산
y_valid_pred = model.predict(X_valid)
valid_rmse = np.sqrt(mean_squared_error(y_valid, y_valid_pred))
print(f"Validation RMSE: {valid_rmse}")

# 테스트 데이터 예측 및 RMSE 계산
y_test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
print(f"Test RMSE: {test_rmse}")
