# 과제5: BMI지수로 비만도 판별하기
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.23

height = float(input("키를 m로 입력하세요: "))
weight = float(input("몸무게를 kg로 입력하세요: "))

def calcBMI(height, weight):
    bmi = weight / (height * height)
    return bmi

def checkBMI(bmi):
    if bmi > 30:
        print(f"당신의 BMI는 {bmi:.1f}이고, 비만입니다.")
    elif bmi > 25:
        print(f"당신의 BMI는 {bmi:.1f}이고, 정상입니다.")
    elif bmi > 18:
        print(f"당신의 BMI는 {bmi:.1f}이고, 저체중입니다.")
        
result = calcBMI(height,weight)
checkBMI(result)