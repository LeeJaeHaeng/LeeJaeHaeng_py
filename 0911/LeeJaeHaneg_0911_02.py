# 과제1: 리스트, 튜플, 딕셔너리
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.11
a = [10, 20, 30, "선문대학교", 3.14, True]
b = 10, 20, 30, "선문대학교", 3.14, True
c = (10, 20, 30, "선문대학교", 3.14, True)
d = {10, 20, 30, "선문대학교", 3.14, True}
e = list(d)

print(a, type(a))
print(b, type(b))
print(c, type(c))
print(d, type(d))

print(a[3][0])
print(b[3][0])
print(c[3][0])
#print(d[3][0])
