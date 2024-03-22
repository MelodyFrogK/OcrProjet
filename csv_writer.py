import csv
import os
from datetime import datetime

# 한글 키 맵핑 및 위치 기반 추출 정의
# '남은기간' 항목을 제거합니다.
KEY_MAP = {
    '발급번호': 6,
    '성명': 10,  # '성명'의 위치는 주민등록번호 바로 다음으로 가정
    '주민등록번호': 11,
    '유효기간': 21,  # '유효기간'의 위치는 세균성이질, 장티프스 등이 나오기 전으로 가정
    '세균성이질': 20,  # '세균성이질' 결과의 위치
    '장티프스': 25,  # '장티프스' 결과의 위치
    '파라티푸스': 30,  # '파라티푸스' 결과의 위치
    '폐결핵': 35,  # '폐결핵' 결과의 위치
}

def extract_data(text_list):
    """
    주어진 텍스트 리스트에서 위치 기반으로 데이터를 추출합니다.
    """
    data = {}
    for key, position in KEY_MAP.items():
        if position < len(text_list):
            data[key] = text_list[position]

    # '유효기간'에서 남은 날짜 계산하여 '남은기간'에 추가
    if '유효기간' in data:
        validity_date = datetime.strptime(data['유효기간'], '%Y-%m-%d')
        today = datetime.now()
        remaining_days = (validity_date - today).days
        if remaining_days < 0:
            data['남은기간'] = '갱신필요'
        else:
            data['남은기간'] = f"{remaining_days}일"

    return data

def append_data_to_csv(data, csv_file_path):
    """
    추출된 데이터를 CSV 파일에 추가합니다.
    """
    file_exists = os.path.isfile(csv_file_path)
    # '남은기간'을 필드명에 추가합니다.
    fieldnames = list(KEY_MAP.keys()) + ['남은기간']
    with open(csv_file_path, mode='a', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)
