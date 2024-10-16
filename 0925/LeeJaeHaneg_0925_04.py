import math

def binary_digits(n):
    count = 1
    while n > 1:
        count += 1
        n = n // 2
    return count

n = int(input("자연수 n을 입력하세요: "))
bit_count = binary_digits(n)
log_value = math.log2(n)

print(f"총 비트수({n}) = {bit_count}")
print(f"log2({n})은 {log_value:.2f}")  # 소수점 둘째 자리까지 출력
