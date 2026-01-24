import sqlite3

def view_data():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, summary, url, created_at FROM news ORDER BY created_at DESC')
    rows = cursor.fetchall()

    conn.close()

    for row in rows:
        print("-" * 50)
        print(f"번호: {row[0]} | 수집시간: {row[4]}")
        print(f"제목: {row[1]}")
        print(f"요약: {row[2]}")
        print(f"URL: {row[3]}")

if __name__ == "__main__":
    print("저장된 뉴스 보기")
    view_data()
