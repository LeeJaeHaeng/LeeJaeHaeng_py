def string_matching(T, P):
    # T는 입력, P는 패턴
    n = len(T)  # n: 입력 문자열의 길이
    m = len(P)  # m: 패턴 문자열의 길이
    for i in range(n - m + 1):  # i: 0, 1, ..., n-m
        j = 0
        while j < m and T[i + j] == P[j]:  # 문제(1): 패턴 문자열을 모두 비교
            j = j + 1
        if j == m:  # 모든 문자가 일치하면, 매칭 성공
            return i  # 현재 위치 반환
    return -1  # 문자열 매칭 실패

text = 'HELLO WORLD'
pattern = 'LO'
print(pattern, 'in', text, '-->', string_matching(text, pattern))

pattern = 'HI'
print(pattern, 'in', text, '-->', string_matching(text, pattern))
