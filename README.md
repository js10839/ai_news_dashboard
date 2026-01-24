# AI 뉴스 요약 대시보드 (AI News Aggregator)

네이버 뉴스(IT/과학)를 자동으로 수집(Crawling)하고, OpenAI GPT를 활용해 3줄로 요약한 뒤, 웹 대시보드에서 보여주는 프로젝트입니다.

## 주요 기능
1. **데이터 수집**: `requests`, `BeautifulSoup`을 사용하여 최신 뉴스 기사 자동 크롤링
2. **AI 요약**: OpenAI API (`gpt-4o-mini`)를 연동하여 긴 본문을 3줄 핵심 요약
3. **데이터 저장**: `SQLite`를 사용하여 기사 원문 및 요약본 영구 저장 (중복 방지 처리)
4. **웹 대시보드**: `FastAPI` + `Jinja2`를 활용한 반응형 뉴스 피드 UI 제공

## 기술 스택 (Tech Stack)
- **Language**: Python 3.10+
- **Web Framework**: FastAPI, Jinja2
- **Database**: SQLite
- **AI/ML**: OpenAI API
- **Crawler**: Requests, BeautifulSoup4

## 프로젝트 구조
- NewsDashboard
    - static/ # CSS 및 정적 파일
        - templates/ # HTML 템플릿
    - app.py # web server
    - crawler.py # crawler
    - summarizer.py # summarizing feature
    - database.py # creating and managing database
    - main.py # main run server
    - news.db # database