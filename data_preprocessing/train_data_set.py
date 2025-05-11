pip install pandas
import pandas as pd

# 파일 불러오기
df_a = pd.read_csv("a.csv")
df_b = pd.read_csv("b.csv")
df_c = pd.read_csv("c.csv")
df_d = pd.read_csv("d.csv")
df_e = pd.read_csv("e.csv")

# 파일 합치기
result = pd.merge(df_a, df_b, on=['index', '시설명', 'address', 'size', 'user', 'latitude', 'longitude'])
result = pd.merge(result, df_c, on=['index', '시설명', 'address', 'size', 'user', 'latitude', 'longitude'])
result = pd.merge(result, df_d, on=['index', '시설명', 'address', 'size', 'user', 'latitude', 'longitude'])
result = pd.merge(result, df_e, on=['index', '시설명', 'address', 'size', 'user', 'latitude', 'longitude'])

# 결과 확인
print(result)

# 결과 저장
result.to_csv("combined.csv", index=False)
