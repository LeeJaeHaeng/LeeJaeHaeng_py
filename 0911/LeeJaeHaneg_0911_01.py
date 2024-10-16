# 과제1: while 반복문, break keyward continue 키워드
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.11
count = 0

while True:
    count += 1
    if count % 2 != 0:  # 홀수일 경우
        continue  # 다음 반복으로 넘어감
    print(count, "회 선문대학교 사랑합니다.")
    if count >= 10:
        break
