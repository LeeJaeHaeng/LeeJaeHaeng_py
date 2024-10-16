# 과제3: 입력한 3개의 정수 중에서 가장 큰 값 찾기
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.23

a = int(input("숫자 a:"))
b = int(input("숫자 b:"))
c = int(input("숫자 c:"))

def getMax(a,b,c):
    if(a>=b) and (a>=c):
        largeNumber = a
    elif(b>=a) and (b>=c):
        largeNumber = b
    else:
        largeNumber = c
        return largeNumber
    
print("가장 큰 수는 ", getMax(a,b,c))