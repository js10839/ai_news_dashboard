import time
import crawler
import summarizer
import db

def RunDashboard():
    print('뉴스 요약 대시보드 시작')
    db.init_db()

    print("1. 뉴스 스크롤...")
    example_main_url = "https://news.naver.com/section/105"
    example_urls = crawler.GetNewsList(example_main_url)
    print(f'총 {len(example_urls)}개의 뉴스 발견')

    for i,url in enumerate(example_urls):
        print(f"\n{i+1}번째 뉴스 크롤링 중... {url}")
        news_data = crawler.GetNewsContent(url)
        if not news_data:
            print("-> 수집 실패, 건너뜁니다.")
            continue

        print(f'제목: {news_data["title"]}')

        print('2. 뉴스 요약...')
        news_summary = summarizer.NewsSummarizer(news_data['content'])

        if news_summary:
            print(f'요약 결과: \n{news_summary}')

        print('3. DB 저장...')
        db.save_news(
            title = news_data['title'],
            content = news_data['content'],
            summary = news_summary,
            url = news_data['url']
        )
        
        time.sleep(1)

        if i == 4:
            break

if __name__ == "__main__":
    RunDashboard()

