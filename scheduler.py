import schedule, time, main
from datetime import datetime

def job():
    print("스케줄러가 뉴스를 크롤링하고 요약합니다:", datetime.now())
    main.RunDashboard()
    print("작업 완료:", datetime.now())

# 매주 월요일 아침 원하는 시간에 실행
# schedule.every().monday.at('09:00').do(job)
# schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
