# 과제9: 실제 실행시간 측정하기(피보나치 수열 - 재귀호출)
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.23

import time
n = int(input("n을 입력하세요: "))

counter = 0

def fibo (n):
    global counter
    counter += 1
    
    if n==1 or n==2:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

start = time.time()
fibo(n)
end = time.time()

print("--------------------------------------")
print(f"fibo({n}) 계산에 활용된 뎃셈 횟수는 {counter}번 입니다.")
print("실행시간=", end - start)