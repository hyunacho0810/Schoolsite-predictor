import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor

# 데이터 불러오기
resampling_data = pd.read_csv('매출액사업체수_resampling.csv')
input_data = pd.read_csv('미호분교_매출액사업체수.csv')

# 학습 데이터 전처리
resampling_data["baby"] = resampling_data["under10"] + resampling_data["10"]
resampling_data = resampling_data.drop(["under10", "10"], axis=1)
resampling_data["young"] = resampling_data["20"] + resampling_data["30"]
resampling_data = resampling_data.drop(["20", "30"], axis=1)
resampling_data["middle"] = resampling_data["40"] + resampling_data["50"] + resampling_data["60"]
resampling_data = resampling_data.drop(["40", "50", "60"], axis=1)
resampling_data["old"] = resampling_data["70"] + resampling_data["80"] + resampling_data["90"]
resampling_data = resampling_data.drop(["70", "80", "90"], axis=1)

# 예측 데이터 전처리
input_data["baby"] = input_data["under10"] + input_data["10"]
input_data = input_data.drop(["under10", "10"], axis=1)
input_data["young"] = input_data["20"] + input_data["30"]
input_data = input_data.drop(["20", "30"], axis=1)
input_data["middle"] = input_data["40"] + input_data["50"] + input_data["60"]
input_data = input_data.drop(["40", "50", "60"], axis=1)
input_data["old"] = input_data["70"] + input_data["80"] + input_data["90"]
input_data = input_data.drop(["70", "80", "90"], axis=1)

# 특성과 타겟 분리
X_train = resampling_data.drop(columns=['user'])
y_train = resampling_data['user']
X_predict = input_data

# 모델 학습
exported_pipeline = ExtraTreesRegressor(bootstrap=False, max_features=0.85, min_samples_leaf=2, min_samples_split=4, n_estimators=100, random_state=42)
exported_pipeline.fit(X_train, y_train)

# 예측 수행
predictions = exported_pipeline.predict(X_predict)
input_data['predicted_user'] = predictions
print(input_data)