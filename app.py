from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

def GetAllNews():
    conn = sqlite3.connect('news.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()

    return rows

@app.get('/')
def ReadRoot():
    return {'message': 'Welcome to the News Summary API'}

@app.get('/News', response_class=HTMLResponse)
def ReadNews(request: Request):
    news_list = GetAllNews()
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'news_list': news_list
        }
    )
