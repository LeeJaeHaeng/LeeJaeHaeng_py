#제목: 원의 둘레와 넓이 구하기(키보드 입력)
pi = 3.1415922654   
r = int(input("반지름 r을 입력하세요: "))
    
print("원주율 = ", pi)
print("반지름 = ", r)
#print("원의 둘레:=",2*pi*r)
#print("원의 둘레 + {:.2f".format}")
print(f"원의 둘레 = {2*r*pi: .2f}")
print(f"원의 넓이 = {r**2*pi:.2f}")