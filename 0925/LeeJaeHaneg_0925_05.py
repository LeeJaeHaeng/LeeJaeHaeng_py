count_r = 0
count_i = 0

def factorial(n):
    global count_r
    count_r += 1
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def factorial_iter(n):
    global count_i
    count_i += 1
    result = 1
    for k in range(1, n + 1):
        result *= k
        count_i += 1  # 반복할 때마다 호출 횟수 증가
    return result

n = int(input("정수 n을 입력하세요: "))

print(f"재귀 Factorial({n}) = {factorial(n)}, 호출횟수: {count_r}")
print(f"반복 Factorial({n}) = {factorial_iter(n)}, 호출횟수: {count_i}")
