# 상권 분석석
import geopandas as gpd             #반경원 코드
import pandas as pd
from shapely.geometry import Point


# 데이터 파일 읽기
facility_data = pd.read_csv('/content/평가_지역_전시_나이.csv')
transit_data = pd.read_csv('/content/_상권데이터 필터링_병합.csv')

# 시설 데이터를 GeoDataFrame으로 변환
facility_gdf = gpd.GeoDataFrame(facility_data, geometry=gpd.points_from_xy(facility_data['longitude'], facility_data['latitude']))

# 대중교통 시설 데이터를 GeoDataFrame으로 변환
transit_gdf = gpd.GeoDataFrame(transit_data, geometry=gpd.points_from_xy(transit_data['longitude'], transit_data['latitude']))


# 결과를 저장할 변수 초기화
transit_count_within_radius = []

# 시설마다 반경 내에 있는 대중교통 시설 수 계산
for facility_index, facility_row in facility_gdf.iterrows():
    facility_point = facility_row.geometry
    radius_meters = 9000

    # 반경원 생성
    facility_buffer = facility_point.buffer(radius_meters / 111000)  # 1도당 약 111km

    # 대중교통 시설 필터링
    transit_within_radius = transit_gdf[transit_gdf.geometry.within(facility_buffer)]

    # 결과 저장
    transit_count_within_radius.append(len(transit_within_radius))


# 기존의 공연시설 데이터에 대중교통 수를 추가
facility_data['Store'] = transit_count_within_radius     #Library, Gallery

# 결과를 나타내는 CSV 파일로 저장
facility_data.to_csv('평가_지역_전시_상권.csv', index=False)