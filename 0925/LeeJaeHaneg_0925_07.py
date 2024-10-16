import math

count = 0

def binary_digits(n):
    global count
    count += 1
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return 1 + binary_digits(n // 2)

n = int(input("자연수 n을 입력하세요: "))
bit_count = binary_digits(n)

print(f"총 비트수 ({n}) = {bit_count}")
print(f"함수 호출 횟수: {count}")
print(f"log2({n})은 {math.log2(n):.4f}")
