# auth.py (새로 생성)
from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectReponses
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
import templates
import sqlite3

# 1. 설정값
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# 2. 도구 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
router = APIRouter()


# 3. 데이터 모델
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: Optional[str] | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


# 4. DB 관련 함수 (fake_users_db 대체)
def get_user(username: str):
    conn = sqlite3.connect('news.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return UserInDB(**user)
    return None


# 5. 인증 관련 함수들
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

import re
def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    
    
# Cookies
async def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    if token.startswith("Bearer "):
        token = token[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except JWTError:
        return None
    
    
# 라우터
@router.get('/login', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.post('/login', response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user(username=username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse('login.html', 
                                          {request: request, 'msg': 'Invalid credentials'})
    access_token = create_access_token(data={'sub': user.username})

    response = RedirectReponses(url='/', status_code=302)
    response.set_cookie(
        key='access_token',
        value=f"Bearer {access_token}",
        httponly=True,
        )
    return response

@router.get('/logout')
def logout():
    response = RedirectReponses(url='/auth/login', status_code=302)
    response.delete_cookie(key='access_token')
    return response
    

# 회원가입
class UserCreate(BaseModel):
    username: str
    password: str
    email: str = None

@router.post("/signup")
def signup(user: UserCreate):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    try:
        hashed_pw = pwd_context.hash(user.password)
        cursor.execute("INSERT INTO users (username, hashed_password, email) VALUES (?, ?, ?)", 
                       (user.username, hashed_pw, user.email))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()
    return {"msg": "User created successfully"}