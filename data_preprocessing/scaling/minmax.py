from sklearn.preprocessing import MinMaxScaler
# MinMaxScaler 객체를 생성합니다.
train_X_num=train[['Total_sales_amount',"baby",'청년','장년층','노년층']]
minmax_scaler = MinMaxScaler()

# fit_transform()을 사용해서 학습과 스케일링을 한 번에 적용합니다.
train_minmax = minmax_scaler.fit_transform(train_X_num)
# Min-Max 스케일링이 완료된 데이터를 데이터프레임 형태로 변환합니다.
train_minmax = pd.DataFrame(train_minmax,
                            index=train_X_num.index,
                            columns=train_X_num.columns)
# 스케일링이 잘 되었는지 데이터를 확인해봅시다.
train_minmax.head()