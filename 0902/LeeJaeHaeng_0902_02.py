#과제2: 리스트에 데이터를 입력하고 최댓값 찾기
#이름: 컴퓨터공학부 이재행

def find_max(A):
    max = A[0]
    for i in range(len(A)):
        if A[i] > max :
            max = A[i]
    return max

