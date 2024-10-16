a = [32, 14, 5, 17, 23, 9, 11, 4, 26, 29]

def seq_search(a, key):
    count = 0  # 비교 횟수를 저장할 변수
    for i in range(len(a)):
        count += 1  # 비교 횟수 증가
        if a[i] == key:
            return i, count  # 인덱스와 비교 횟수 반환
    return -1, count  # 찾지 못했을 경우 -1과 비교 횟수 반환

key = int(input("찾고자 하는 key 번호를 입력하세요: "))
index, comparisons = seq_search(a, key)

print(f"리스트 a의 크기: {len(a)}, 비교횟수: {comparisons}")
