
import os
import jwt


from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",10080))
ALGORITHM ="HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(plain_password, password):
    return pbkdf2_sha256.verify(plain_password, password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now().astimezone() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)    

def decode_access_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])