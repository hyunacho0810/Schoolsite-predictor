from sklearn.preprocessing import StandardScaler
# StandardScaler객체를 생성합니다.
num=['size',  'Population_woman', 'Population_man', 'transit_count','total', 'baby', '청년', '장년층', '노년층']
train_X_num=train[num]
s_scaler = StandardScaler()

# fit_transform()을 사용해서 학습과 스케일링을 한 번에 적용합니다.
train_standard = s_scaler.fit_transform(train_X_num)
# Min-Max 스케일링이 완료된 데이터를 데이터프레임 형태로 변환합니다.
train_standard = pd.DataFrame(train_standard,
                            index=train_X_num.index,
                            columns=train_X_num.columns)