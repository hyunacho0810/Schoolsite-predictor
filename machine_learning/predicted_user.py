#미호분교의 각 type별로 예상되는 이용자수 도출
import pandas as pd

# 엑셀 파일 불러오기
new_data = pd.read_csv('/content/1번 입력데이터.csv', encoding='cp1252')

# X값에 해당하는 데이터 추출
X_new = new_data[['size','Population_woman','Population_man','under10','10s','20s','30s','40s','50s','60s',
                               '70s','80s','90s','transit_count','number of type0','number of type1','number of type2','number of type3','total','type']]

# 모델을 사용하여 예측 수행
y_new_pred = model.predict(X_new)

# 결과 출력
print("새로운 상황에 대한 예측 결과:")
for i, pred in enumerate(y_new_pred):
    print(f"상황 {i+1}: 예측 이용자 수 = {pred}")
