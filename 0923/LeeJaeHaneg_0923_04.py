# 과제4: 가변 매개변수와 기본 매개변수
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.23

# 가변 매개변수 예제
def n_times(n, *values):
    for i in range(n):
        for v in values:
            print(i, v)
    
print(n_times(3, "선문대", "컴공", "화이팅"))

# 기본 매개변수 예제
def times( *values, n=2):
    for i in range(n):
        for v in values:
            print(i, v)
    
print(times("선문대", "컴공", "화이팅", n=8))

print("선문대학교", end = " ")
print("컴공",end = " ")
print("화이팅",end = " ")
