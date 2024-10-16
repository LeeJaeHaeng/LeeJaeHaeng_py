n = int(input("n을 입력하세요: "))

for i in range(1, 10):
    for j in range(2, n+1):
        gugudan = f"{j} * {i} = {j * i}"  # 구구단 계산
        print(gugudan, end="\t")  # 탭으로 간격 조정
    print()  # 각 i 값에 대해 줄바꿈