#전체코드
pip install pandas scikit-learn xgboost matplotlib seaborn

import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일을 불러옵니다. 파일 경로를 지정하세요.
file_path = '/content/1번 학습데이터.csv'
data = pd.read_csv(file_path, encoding='cp1252')

# 데이터 확인
print(data.head())

# X 값과 y 값을 지정합니다.
X = data[['size', 'Population_woman', 'Population_man', 'under10', '10s', '20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s', 'transit_count', 'number of type0', 'number of type1', 'number of type2', 'number of type3', 'total', 'type']]
y = data['user']

# 데이터셋을 훈련, 검증, 테스트 세트로 분할합니다.
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f'Training set size: {X_train.shape[0]}')
print(f'Validation set size: {X_valid.shape[0]}')
print(f'Test set size: {X_test.shape[0]}')

# XGBoost 모델을 학습합니다.
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
model.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_valid, y_valid)], verbose=True)

# 모델을 평가합니다.
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print(f'Test RMSE: {rmse}')

# 예측값과 실제값을 비교하는 시각화
def plot_predictions(y_true, y_pred):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_true, y=y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], color='red', linestyle='--', lw=2)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Actual vs Predicted Values')
    plt.show()

# 잔차 그래프 시각화
def plot_residuals(y_true, y_pred):
    residuals = y_true - y_pred
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_pred, y=residuals, alpha=0.5)
    plt.axhline(0, color='red', linestyle='--', lw=2)
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residuals vs Predicted Values')
    plt.show()

# 시각화 함수 호출
plot_predictions(y_test, y_pred)
plot_residuals(y_test, y_pred)
