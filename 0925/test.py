import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로
file_path = 'C:\Users\leejh\Downloads\2024_seoul_bus.csv'  # 여기에 CSV 파일 경로를 입력하세요.

# CSV 파일 읽기
data = pd.read_csv(file_path)

# 데이터의 첫 5행 출력
print(data.head())

# 기본 정보 출력
print(data.info())

# 통계 요약 출력
print(data.describe())

# 특정 열의 값 분포 시각화 (예: 'column_name'을 분석하고 싶은 열 이름으로 변경)
plt.figure(figsize=(10, 6))
data['A'].value_counts().plot(kind='bar')
plt.title('Value Distribution of column_name')
plt.xlabel('Values')
plt.ylabel('Counts')
plt.show()
