# 과제6: lambda 기초 - 익명 함수와 일반 함수의 차이
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.23
power_l = lambda x: x*x

def power_func(a):
    res = a*a
    return res

num = int(input("제곱을 구하고자 하는 숫자를 입력: "))
result = power_func(num)
result2 = power_l(num)

print(f"{num}의 제곱f은 {result}이다.")
print(f"{num}의 제곱l은 {result2}이다.")