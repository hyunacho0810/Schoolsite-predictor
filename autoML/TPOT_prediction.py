import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import MinMaxScaler
from tpot.builtins import StackingEstimator
from xgboost import XGBRegressor
from tpot.export_utils import set_param_recursive
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.inspection import permutation_importance

# 데이터 불러오기
tpot_data = pd.read_csv('log_100_5km_나이X.csv', sep=',', dtype=np.float64)
features = tpot_data.drop('user', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['user'], random_state=42)

# 파이프라인 구성
exported_pipeline = make_pipeline(
    MinMaxScaler(),
    StackingEstimator(estimator=RidgeCV()),
    StackingEstimator(estimator=XGBRegressor(learning_rate=0.001, max_depth=8, min_child_weight=17, n_estimators=100, n_jobs=1, objective="reg:squarederror", subsample=1.0, verbosity=0)),
    KNeighborsRegressor(n_neighbors=49, p=1, weights="distance")
)
# 랜덤 상태 고정
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

# 모델 학습
exported_pipeline.fit(training_features, training_target)

# 예측
results = exported_pipeline.predict(testing_features)

# 모델 성능 측정
r2 = r2_score(testing_target, results)
mae = mean_absolute_error(testing_target, results)
mse = mean_squared_error(testing_target, results)

print(f"R^2: {r2}")
print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")

# 변수 중요도 계산
perm_importance = permutation_importance(exported_pipeline, testing_features, testing_target, n_repeats=10, random_state=42)
feature_names = features.columns
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': perm_importance.importances_mean})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
print("변수 중요도:")
print(importance_df)

# 새로운 데이터 불러오기 및 예측
new_data = pd.read_csv('log_미호분교_5km_나이X.csv', sep=',', dtype=np.float64)
new_features = new_data

# 새로운 데이터에 대해 동일한 스케일링 적용
scaler = MinMaxScaler().fit(training_features)
scaled_new_features = scaler.transform(new_features)

# 새로운 데이터에 대한 예측
new_target_predictions = exported_pipeline.predict(scaled_new_features)

# 로그 역변환 (만약 로그 변환이 사용된 경우)
final_predictions = np.exp(new_target_predictions)

# 예측 결과 출력
print("최종 예측 결과:")
print(final_predictions)
