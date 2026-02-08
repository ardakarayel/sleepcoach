"""
Authentication Helper Modülü
----------------------------
Şifre hash'leme ve JWT Token işlemleri.
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt

# Şifre hash'leme konfigürasyonu (bcrypt kullanıyoruz)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Konfigürasyonu
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "sleepcoach-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7  # Token 7 gün geçerli


# ============================================
# 🔒 ŞİFRE İŞLEMLERİ
# ============================================

def hash_password(password: str) -> str:
    """Şifreyi hash'ler (bcrypt)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Girilen şifre ile hash'lenmiş şifreyi karşılaştırır."""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================
# 🎟️ JWT TOKEN İŞLEMLERİ
# ============================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT Access Token oluşturur."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """JWT Token'ı decode eder. Geçersizse None döner."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """Token'dan user_id çıkarır."""
    payload = decode_access_token(token)
    if payload:
        return payload.get("user_id")
    return None
