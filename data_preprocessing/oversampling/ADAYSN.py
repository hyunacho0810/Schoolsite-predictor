import pandas as pd
from imblearn.over_sampling import ADASYN

# 데이터 파일 로드
file_path = "/Users/syo/Documents/5-1/데애/전처리/오버샘플링_adasyn/filled_train3_시설명제거.csv"
df = pd.read_csv(file_path)

# 'type' 칼럼을 타겟으로 사용
X = df.drop(['type'], axis=1)  # 피처 데이터
y = df['type']  # 타겟 데이터

# 클래스 분포 확인
class_distribution = y.value_counts()
print("Class distribution before resampling:", class_distribution)

# type 1의 샘플 수를 기준으로 샘플링 전략 설정
target_samples = class_distribution[1]

# 샘플링 전략: type 1의 수에 맞추어 type 2와 type 3만 오버샘플
sampling_strategy = {2: target_samples, 3: target_samples}

# ADASYN 오버샘플링 적용
adasyn = ADASYN(sampling_strategy=sampling_strategy, random_state=42, n_neighbors=40)  # n_neighbors는 조정 가능
X_resampled, y_resampled = adasyn.fit_resample(X, y)

# 오버샘플링 후 클래스 분포 확인
new_class_distribution = pd.Series(y_resampled).value_counts()
print("Class distribution after resampling:", new_class_distribution)

# 결과 데이터 프레임 재구성
resampled_df = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.DataFrame(y_resampled, columns=['type'])], axis=1)

# 결과 데이터 저장
resampled_df.to_csv(file_path.replace('.csv', '_resampled3.csv'), index=False)