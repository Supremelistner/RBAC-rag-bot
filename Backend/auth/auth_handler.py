from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

jwt_secret_key = os.getenv("JWT_SECRET_KEY", "your_default_secret_key")
jwt_algorithm ="HS256"
access_token_exp = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=access_token_exp))
    payload = {"exp": expire, "sub": str(subject), "role": role}
    return jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        return payload if payload["exp"] >= int(datetime.now(timezone.utc).timestamp()) else None
    except JWTError:
        return None
