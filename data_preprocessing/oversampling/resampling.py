import pandas as pd
from sklearn.utils import resample

# 파일 불러오기
files = ["공연시설.csv", "전시시설.csv", "지역문화활동시설.csv", "도서시설.csv"]

# 데이터 프레임을 리스트에 저장
dfs = [pd.read_csv(file) for file in files]

# 샘플 수 계산
sample_counts = [len(df) for df in dfs]

# 오버샘플링 적용
resampled_dfs = []
for df, count in zip(dfs, sample_counts):
    if count < 1250:
        # 기존 데이터를 그대로 유지하고 부족한 만큼 오버샘플링
        additional_samples = resample(df, replace=True, n_samples=(1250 - count), random_state=42)
        resampled_df = pd.concat([df, additional_samples])
    else:
        resampled_df = df
    resampled_dfs.append(resampled_df)

# 새로운 파일들을 병합하여 하나의 데이터프레임으로 만듦
merged_df = pd.concat(resampled_dfs, ignore_index=True)

# 최종 파일로 저장
merged_df.to_csv("최종_파일.csv", index=False)

# 파일별 샘플 수 출력
print("각 파일의 샘플 수:")
for i, (file_name, original_count) in enumerate(zip(files, sample_counts)):
    new_count = 1250 if original_count < 1250 else original_count
    print(f"{file_name}: {original_count} -> {new_count}")

# 데이터프레임 확인
print("\n최종 데이터프레임 샘플:")
print(merged_df.head())

# 최종 파일의 전체 샘플 수 출력
print("\n최종 파일의 총 샘플 수:", len(merged_df))