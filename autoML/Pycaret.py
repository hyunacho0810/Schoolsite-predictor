import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pycaret.regression import *

# 데이터 업로드 후 파일 이름 확인
train_filename = list(uploaded.keys())[0]
input_filename = list(uploaded.keys())[1]

train = pd.read_csv(train_filename)
input_data = pd.read_csv(input_filename)

# 미성년자 청년 장년층 노년층으로 묶기
train["baby"] = train["under10"] + train["10대"]
train["청년"] = train["20대"] + train["30대"]
train["장년층"] = train["40대"] + train["50대"] + train["60대"]
train["노년층"] = train["70대"] + train["80대"] + train["90대"]

# 필요없는 열 제거
columns_to_drop = ["under10", "10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대", "90대", "latitude", "longitude"]
train = train.drop(columns=columns_to_drop, axis=1)

# 로그변환
train = train.applymap(lambda x: np.log1p(x) if isinstance(x, (int, float)) else x)

# MinMax 스케일링
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(train.drop("user", axis=1))
scaled_train = pd.DataFrame(scaled_features, columns=train.columns[:-1])
scaled_train["user"] = train["user"]

# PyCaret을 사용하여 모델 학습 (회귀)
reg1 = setup(data=scaled_train, target='user', normalize=True, transformation=True, session_id=123)

# 모델 비교 및 최적 모델 선택
best_model = compare_models()

# 모델 저장
save_model(best_model, 'best_model_pycaret')

# 새로운 데이터에 대한 예측
input_data["baby"] = input_data["under10"] + input_data["10대"]
input_data["청년"] = input_data["20대"] + input_data["30대"]
input_data["장년층"] = input_data["40대"] + input_data["50대"] + input_data["60대"]
input_data["노년층"] = input_data["70대"] + input_data["80대"] + input_data["90대"]
input_data = input_data.drop(columns=columns_to_drop, axis=1)
input_data = input_data.applymap(lambda x: np.log1p(x) if isinstance(x, (int, float)) else x)
input_data_scaled = scaler.transform(input_data)

# 예측
predictions = predict_model(best_model, data=pd.DataFrame(input_data_scaled, columns=input_data.columns))

# 예측 결과 출력
print(predictions)