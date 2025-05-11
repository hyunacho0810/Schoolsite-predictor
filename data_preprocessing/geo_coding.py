import googlemaps
import pandas as pd
from tqdm import tqdm

# 구글 맵 api 로드
mykey = "여기에 키 입력!"   #발급받은 키 입력하기
maps = googlemaps.Client(key=mykey)  #구글맵 api 가져오기

#주소 데이터 파일 임포트(pandas이용)
center = pd.read_csv('/content/평가 데이터.csv')

# trans_geo라는 함수를 정의: 주소(address)를 받아서 위도경도로 반환
def trans_geo(address):   
    try:                                 #geo_location: 이 변수는 구글맵 API의 geocode() 메서드를 통해 반환된 결과
        geo_location = maps.geocode(address)[0].get('geometry')    #maps.geocode(address): 구글맵 api를 사용해 지오코딩하는 부분 [0]은 api응답에서 첫번째 결과를 가져오라는 것
        lat = geo_location['location']['lat']   #위도
        lng =  geo_location['location']['lng']  #경도 
        return [lat,lng]
    except:
        return [0,0]       #예외를 처리하는 부분: 주소 변환하는 중에 오류 발생하면 '0'으로 대체하여 반환

# 실행
for idx, address in enumerate(tqdm(center.address)):      
    center.loc[idx,'latitude'] = trans_geo(address)[0]       #각 주소를 'trans_geo() 함수에 전달해서 위도 가져오기, 이를 내 파일의 데이터프레임의 새로운 열인 latitude에 할당. [0]은 trans_geo() 함수의 반환 값 중 첫 번째 값
    center.loc[idx,'longitude'] = trans_geo(address)[1]      # [1]은 함수 반환값 중 두번째 값

center.to_csv('updated_center.csv', index=False)  