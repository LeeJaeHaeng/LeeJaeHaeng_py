def unique_elements(A):
    n = len(A)
    count = 0  # 비교 횟수를 저장할 변수
    for i in range(n - 1):
        for j in range(i + 1, n):
            count += 1  # 비교 횟수 증가
            if A[i] == A[j]:
                return False, count  # 중복 발견 시 False와 비교 횟수 반환
    return True, count  # 중복이 없을 경우 True와 비교 횟수 반환

A = [32, 14, 5, 17, 23, 9, 11, 14, 26, 29]
B = [13, 6, 8, 7, 12, 25]

result_A, count_A = unique_elements(A)
result_B, count_B = unique_elements(B)

print(f"{A} 중복 여부: {result_A}, 비교횟수: {count_A}")
print(f"{B} 중복 여부: {result_B}, 비교횟수: {count_B}")
