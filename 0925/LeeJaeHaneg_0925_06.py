# 하노이 탑

count = 0

def hanoi_tower(n, fr, tmp, to):
    global count
    count += 1
    if n == 1:
        print(f"원판 1: {fr} --> {to}")
    else:
        hanoi_tower(n-1, fr, to, tmp)
        print(f"원판 {n}: {fr} --> {to}")
        hanoi_tower(n-1, tmp, fr, to)

n = int(input("원반의 개수 n(자연수)를 입력하세요: "))
hanoi_tower(n, 'A', 'B', 'C')
print(f"함수 호출 횟수: {count}")
