import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 데이터셋 불러오기
data = pd.read_csv('/content/1번 학습데이터.csv', encoding='cp1252')

# X (독립 변수)와 y (종속 변수) 정의
X = data[['size','Population_woman','Population_man','under10','10s','20s','30s','40s','50s','60s',
                       '70s','80s','90s','transit_count','number of type0','number of type1','number of type2','number of type3','total','type']]
y = data['user']

# 데이터셋을 train, validation, test로 나누기
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# 모델 정의 및 학습
model = LinearRegression()
model.fit(X_train, y_train)

# 검증 세트로 예측
y_valid_pred = model.predict(X_valid)

# 모델 평가
mse = mean_squared_error(y_valid, y_valid_pred)
r2 = r2_score(y_valid, y_valid_pred)

print(f"Validation MSE: {mse}")
print(f"Validation R2: {r2}")

# 테스트 세트로 예측
y_test_pred = model.predict(X_test)

# 모델 평가
mse_test = mean_squared_error(y_test, y_test_pred)
r2_test = r2_score(y_test, y_test_pred)

print(f"Test MSE: {mse_test}")
print(f"Test R2: {r2_test}")