# 과제1: 리스트, 튜플, 딕셔너리
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.11
def sunmoon():
    return(11,12,13,14)

aaa=sunmoon()
print(sunmoon(),type(sunmoon()))
print(aaa[0], type(aaa[0]))

[a,b] = [10, 20]
(c,d) = (10,20)
e = [100, 200, 300, 400]
f = 101, 201, 301,401
a,b = b,a
print('a:', a, 'type=', type(a))
print('b:', a, 'type=', type(b))
print('c:', a, 'type=', type(c))
print('d:', a, 'type=', type(d))
print('e:', a, 'type=', type(e))
print('f:', a, 'type=', type(f))

print(e[1])
print(f[1])