import pandas as pd
from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import numpy as np

# 데이터 불러오기
train_data = pd.read_csv('log_transformed_data.csv')


# 피처와 타겟 분리
X = train_data.drop(columns=['user'])
y = train_data['user']

# 피처와 타겟 모두 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y.values.reshape(-1, 1)).flatten()  # y는 1차원이므로 reshape 후 flatten

# 데이터셋 분할
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, train_size=0.75, test_size=0.25, random_state=42)

# TPOT 모델 생성 및 학습
tpot = TPOTRegressor(
    generations=10,
    population_size=50,
    verbosity=2,
    scoring=make_scorer(r2_score),  # 단일 메트릭 사용
    random_state=42,
    cv=5,
    n_jobs=-1
)

tpot.fit(X_train, y_train)

# 최적화된 모델의 평가 지표 계산 및 출력
y_pred = tpot.predict(X_test)
r_squared = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print("최적화된 모델의 평가 지표:")
print("R-squared on test set:", r_squared)
print("MAE on test set:", mae)
print("MSE on test set:", mse)
print("MAPE on test set:", mape)

# 최적화된 모델을 코드로 export
tpot.export('tpot_10_pipeline.py')