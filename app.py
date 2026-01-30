from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from login import router as auth_router, get_current_user_from_cookie
import sqlite3
import db

app = FastAPI()
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
db.init_db()

def GetAllNews():
    conn = sqlite3.connect('news.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()

    return rows

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/auth/login", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: str = Depends(get_current_user_from_cookie)):
    if user is None:
        return RedirectResponse(url="/auth/login", status_code=302)

    news_list = GetAllNews()
    return templates.TemplateResponse("index.html", {"request": request, "news_list": news_list})

