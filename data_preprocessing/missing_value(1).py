culture=pd.read_csv("/content/drive/MyDrive/지역문화활동시설_merged f.csv")
art=pd.read_csv("/content/drive/MyDrive/전시시설_merged.csv")
play=pd.read_excel("/content/공연시설_merged (1).xlsx")
play1=pd.read_excel("/content/drive/MyDrive/공연시설명.xlsx")
book=pd.read_csv("/content/drive/MyDrive/도서시설_merged.csv")

#중복값 제거
culture.info()
culture=culture.drop("address",axis=1)

#size, user 항목에 단위 포함되거나 오류? 난 부분 제거
import re
#size중에 문자제거 숫자만 남김
def extract_numbers(string):
    if isinstance(string, str):
        return re.sub(r'[^\d.]', '', string)
    else:
        return ''

# culture["size"] 열의 각 항목에 함수를 적용하여 숫자와 소수점만 추출하고 열을 업데이트합니다.
culture["size"] = culture["size"].apply(extract_numbers)
culture["user"] = culture["user"].apply(extract_numbers)

culture["size"] = culture["size"].replace('', pd.NA)
culture["size"] = pd.to_numeric(culture["size"], errors='coerce')

culture["user"] = culture["user"].replace('', pd.NA)
culture["user"] = pd.to_numeric(culture["user"], errors='coerce')