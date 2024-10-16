# 과제8: matplotlib(외부모듈) 막대그래프와 파이차트 그리기
# 이름: 컴퓨터공학부 이재행
# 날짜: 24.09.23
import matplotlib.pyploat as plt

x = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sun"]
Y1 = [15.6, 14.2, 16.3, 18.2, 17.1, 20.2, 22.4]
Y2 = [20.1, 23.1, 23.8, 25.9, 23.4, 25.1, 26.3]

Y3 = [40, 20, 10, 30]
Y3_labels = ["Eating Out", "Shopping", "Groceries", "Housing"]

#막대그래프
plt.bar(X,Y1)
plt.show()

#파이차트
explode = [0,1,0,0,0]
plt.pie(Y3, labels=Y3_labels, explode = explode)

plt.show()