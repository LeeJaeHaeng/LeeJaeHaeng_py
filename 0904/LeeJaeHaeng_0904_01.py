#과제1: 유클리드 호제법(최대공약수 구하기)
#이름: 컴퓨터공학부 이재행

def gcd(a,b):
    print("gcd", (a,b))
    while b != 0:
        r = a % b
        a = b
        b = r
        print("gcd", (a,b))
    return a
a = int(input("a 정수를 입력하세요:"))
b = int(input("b 정수를 입력하세요:"))
print("60과 28의 최대 공약수 =", gcd(60, 28))