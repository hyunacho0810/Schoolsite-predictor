import geopandas as gpd   # 지리 공간 데이터를 다루는 데 사용되는 라이브러리
import pandas as pd
from shapely.geometry import Point # Shapely는 파이썬에서 지오메트리 연산을 수행하는 데 사용되는 라이브러리


# 데이터 파일 읽기
facility_data = pd.read_csv('/content/도서시설_file.csv')
transit_data = pd.read_csv('/content/KC_496_LLR_PPLTEQP_2023.csv')

# 시설 데이터를 GeoDataFrame으로 변환 Pandas DataFrame으로부터 GeoPandas의 GeoDataFrame을 만들고, 시설의 위도(latitude)와 경도(longitude)를 이용해 각 시설을 지리적인 점(Point)으로 표현
facility_gdf = gpd.GeoDataFrame(facility_data, geometry=gpd.points_from_xy(facility_data['longitude'], facility_data['latitude']))

# 대중교통 시설 데이터를 GeoDataFrame으로 변환
transit_gdf = gpd.GeoDataFrame(transit_data, geometry=gpd.points_from_xy(transit_data['LC_LO'], transit_data['LC_LA']))

# 결과를 저장할 변수 초기화
transit_count_within_radius = []

# 시설마다 반경 내에 있는 대중교통 시설 수 계산
for facility_index, facility_row in facility_gdf.iterrows():
    facility_point = facility_row.geometry
    radius_meters = 450

    # 반경원 생성
    facility_buffer = facility_point.buffer(radius_meters / 111000)  # 1도당 약 111km

    # 대중교통 시설 필터링
    transit_within_radius = transit_gdf[transit_gdf.geometry.within(facility_buffer)]

    # 결과 저장
    transit_count_within_radius.append(len(transit_within_radius))


# 기존의 공연시설 데이터에 대중교통 수를 추가
facility_data['transit_count'] = transit_count_within_radius

# 결과를 나타내는 CSV 파일로 저장
facility_data.to_csv('시설_대중교통수_결과.csv', index=False)