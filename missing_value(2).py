from sklearn.impute import KNNImputer

#임퓨터 선언(5개의 평균으로 계산하겠다)
imputer=KNNImputer(n_neighbors=5)

#임퓨터를 사용하여 filled_train으로 저장 이후 
#같은 임퓨터를 사용할때는 imputer.transform()으로 사용하면됨
filled_train=imputer.fit_transform(fill1)

#사용하면 array값으로 나오기때문에 dataframe으로 바꿔주고 컬럼을가져옴
filled_train=pd.DataFrame(filled_train, columns=fill1.columns)