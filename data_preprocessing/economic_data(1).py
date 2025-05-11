# 매출액, 사업체 수 분석 
from math import radians, cos, sin, sqrt, atan2
import csv

# 하버사인 공식을 사용하여 두 점 간의 거리를 계산하는 함수
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구의 반지름 (km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 문화시설 파일과 통계 데이터 파일의 경로
cultural_facilities_file = '/content/지역문화활동시설_merged_수정.csv' #수정필요!!!!
statistical_data_file = '/content/산업대분류별 총괄.csv'

# 모든 시설에 공통적으로 사용할 반경 거리 설정
fixed_radius_km = 1.0  #수정필요!!!!!!

# 문화시설 정보를 로드
cultural_facilities = []
with open(cultural_facilities_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    headers = reader.fieldnames + ['Total_sales_amount']  # 기존 컬럼에 총 인구수 컬럼 추가
    for row in reader:
        facility = {
            **row,  # 기존 데이터를 모두 복사
            'latitude': float(row['latitude']),
            'longitude': float(row['longitude'])
        }
        cultural_facilities.append(facility)

# 통계 데이터를 로드
statistical_data = []
with open(statistical_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        statistical_data.append({
            'latitude': float(row['latitude']),
            'longitude': float(row['longitude']),
            'sales_amount': int(row['sales_amount'])     #sales_amount
        })

# 각 문화시설마다 근처 통계 값 합산 및 결과 CSV 작성
output_data = []
for idx, facility in enumerate(cultural_facilities, start=1):
    total = 0
    for entry in statistical_data:
        distance = haversine(facility['latitude'], facility['longitude'], entry['latitude'], entry['longitude'])
        if distance <= fixed_radius_km:
            total += entry['sales_amount']
    output_row = {'Index': idx, **facility, 'Total_sales_amount': total}
    output_data.append(output_row)

# 결과를 CSV 파일로 저장
output_csv_file = '지역문화활동시설_매출액.csv'  #수정필요!!!!!!!!
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Index'] + headers)
    writer.writeheader()
    writer.writerows(output_data)

print(f"Results written to {output_csv_file}")
