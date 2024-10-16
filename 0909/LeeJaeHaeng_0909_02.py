#제목: 현재 날짜와 시간 출력
import datetime

now = datetime.datetime.now()

print(now.year, "년")
print(now.month, "월")
print(now.day, "일")
print(now.hour, "시")
print(now.minute, "분")
print(now.second, "초")

current_1 = "{}년 {}월 {}일 {}시 {}분 {}초".format(
    now.year, now.month, now.day, now.hour, now.minute, now.second
)
print(current_1)

current_2 = f"{now.year}년 {now.month}월 {now.day}일 \
    {now.hour}시 {now.minute}분 {now.second}초"
print(current_2)

