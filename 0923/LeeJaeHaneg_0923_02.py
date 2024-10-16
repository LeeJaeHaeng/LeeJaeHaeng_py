# 과제2: 1~n까지 x배수의 합을 구하는 함수
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.23

n = int(input("까지 n 입력: "))
x = int(input("배수 x 입력: "))

def sum_x(n, x): # 함수의 정의
    sum  = 0
    for i in range(1, n + 1):
        if i%x == 0:
            sum = sum + i
            print("i =",i, "sum =", sum)
            
sum_x(n,x) # 함수의 호출