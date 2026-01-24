import sqlite3
import datetime

DB_NAME = 'news.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            summary TEXT,
            url TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Dtabase initialized.")

def save_news(title, content, summary, url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # 중복 뉴스 스킵
        cursor.execute(
            '''
            INSERT OR IGNORE INTO news (title, content, summary, url) VALUES (?, ?, ?, ?)
            ''', (title, content, summary, url)
        )

        conn.commit()
        if cursor.rowcount > 0:
            print(f"Saved Successfully: {title}")
        else:
            print(f"Already Exists: {title}")
        
    except Exception as e:
        print(f"Error saving news: {e}")
    finally:
        conn.close()
if __name__ == "__main__":
    init_db()
    # 가짜 데이터로 테스트
    save_news("테스트 제목", "테스트 내용입니다", "세줄요약입니다", "http://test.com/1")
