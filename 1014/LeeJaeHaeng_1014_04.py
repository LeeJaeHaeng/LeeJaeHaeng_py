def sequential_search(A, key):
    # A는 입력 리스트, key는 찾으려는 값
    for i in range(len(A)):  # i : 0, 1, 2, ..., len(A)-1
        if A[i] == key:  # 문제(1): 탐색 성공하면 (비교 연산)
            return i + 1  # 인덱스에 1을 더하여 반환
    return -1  # 탐색에 실패하면 -1 반환

A = [32, 14, 5, 17, 23, 9, 11, 4, 26, 29]

print(f"리스트 A : {A}")
print(f"리스트 A 크기: {len(A)}")

key = 11  # 찾고 싶은 값
num = sequential_search(A, key)  # 문제(2): 함수 호출하여 key를 찾음

print(f"순차 탐색 횟수: {num}")  # 문제(3): 결과 출력
