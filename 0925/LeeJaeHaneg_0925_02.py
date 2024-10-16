def computer_square_A(n):
    count = 0
    count += 1
    return n * n, count

def computer_square_B(n):
    sum = 0
    count = 0
    for i in range(n):
        sum = sum + n
        count += 1
    return sum, count

def computer_square_C(n):
    sum = 0
    count = 0
    for j in range(n):
        sum = sum + n
        count += 1
    return sum, count

n = int(input("정수 n을 입력하세요: "))

result_A, count_A = computer_square_A(n)
result_B, count_B = computer_square_B(n)
result_C, count_C = computer_square_C(n)

print(f"알고리즘 A 결과: {result_A}, 횟수: {count_A}")
print(f"알고리즘 B 결과: {result_B}, 횟수: {count_B}")
print(f"알고리즘 C 결과: {result_C}, 횟수: {count_C}")
