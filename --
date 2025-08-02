from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Dict
from jose import jwt
from passlib.context import CryptContext

app = FastAPI()

# JWT Ayarları
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Sahte kullanıcı veritabanı
fake_users_db: Dict[str, Dict] = {}

# Şifreleme ayarları
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Kullanıcı oluşturma modeli
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# JWT token modeli
class Token(BaseModel):
    access_token: str
    token_type: str

# Şifre hashleme fonksiyonu
def get_password_hash(password):
    return pwd_context.hash(password)

# Şifre doğrulama fonksiyonu
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Token oluşturma fonksiyonu
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Kayıt endpointi
@app.post("/register", response_model=Token)
def register(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten var")
    hashed_pw = get_password_hash(user.password)
    fake_users_db[user.email] = {"email": user.email, "hashed_password": hashed_pw}
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Giriş endpointi
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Geçersiz giriş bilgisi")
    token = create_access_token(data={"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
