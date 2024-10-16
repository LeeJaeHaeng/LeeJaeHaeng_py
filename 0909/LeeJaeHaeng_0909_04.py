#홀수와 /작수 나머지 연산자(%)로 구분하기

#입력
number = input("정수 입력: ")
number = int(number)

if number % 2 == 0:
    print(f"{number}은 짝수")
    
if number % 2 == 1:
    print(f"{number}은 홀수")