import requests
from bs4 import BeautifulSoup
import time


def GetNewsContent(url):
    # 1. 서버에 "이 주소의 내용을 줘"라고 요청을 보냅니다.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # 요청이 성공했는지 확인
    if response.status_code != 200:
        raise Exception(f"접속 실패!! {url}")
    
    # 2. 가져온 HTML(웹페이지 소스)을 BeautifulSoup으로 정리
    soup = BeautifulSoup(response.text, "html.parser")

    # 3. 제목과 본문을 찾아서 추출합니다.
    title_tag = soup.select_one("#title_area")
    content_tag = soup.select_one("#dic_area")

    if title_tag and content_tag:
        title = title_tag.text.strip()
        content = content_tag.text.strip()

        return {
            'title': title,
            'content': content,
            'url': url
        }
    else:
        print('제목이나 본문을 찾지 못했습니다.')
        return None
    
def GetNewsList(section_url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(section_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 네이버 뉴스 '섹션' 페이지에서 기사 제목(링크)들을 모두 찾습니다.
    news_links = soup.select('a.sa_text_title')
    news_urls = []

    for link in news_links:
        url = link['href']
        if url.startswith("http"):
            news_urls.append(url)
    
    return news_urls

    
# if __name__ == "__main__":
#     example_main_url = "https://news.naver.com/section/105"
#     print("뉴스 크롤링 시작")

#     example_urls = GetNewsList(example_main_url)
#     print(f'총 {len(example_urls)}개의 뉴스 발견')

    # for i,url in enumerate(example_urls):
    #     print(f"\n{i+1}번째 뉴스 크롤링 중... {url}")
    #     news_data = GetNewsContent(url)
    #     if news_data:
    #         print(f"제목: {news_data['title']}")
    #         print(f"본문 길이: {len(news_data['content'])}자")
    #         # 봇으로 오해받지 않게 1초 쉽니다 (매너)
    #         time.sleep(1)
#         else:
#             print("수집 실패")

#         if i==4:
#             break

#     print("\n테스트 종료!")


