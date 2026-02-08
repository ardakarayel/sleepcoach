from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

try:
    from .database import Base
except ImportError:
    from database import Base


# ============================================
# 👤 USER MODELİ (Kimlik Doğrulama)
# ============================================
class User(Base):
    """
    Kullanıcı hesabı.
    Email ve username benzersiz (unique) olmalı.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişki: Bu kullanıcının uyku oturumları
    sleep_sessions = relationship("SleepSession", back_populates="user", cascade="all, delete-orphan")


# ============================================
# 😴 UYKU OTURUMU MODELİ
# ============================================
class SleepSession(Base):
    __tablename__ = "sleep_sessions"

    id = Column(Integer, primary_key=True, index=True)
    
    # 👤 Kullanıcı İlişkisi (Hangi kullanıcının uyku verisi?)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Şimdilik nullable, migration sonrası zorunlu yapılabilir
    user = relationship("User", back_populates="sleep_sessions")
    
    input_date = Column(DateTime, index=True)  # Verinin sisteme girdiği tarih
    
    # Oturumun genel sınırları
    start_time = Column(DateTime) # Uyku başlangıcı
    end_time = Column(DateTime)   # Uyanış
    
    # Özet Veriler (Dakika cinsinden - işlem için)
    total_sleep_duration = Column(Float, default=0.0) # Sadece uyunan (Deep+REM+Core)
    total_time_in_bed = Column(Float, default=0.0)    # Yatakta geçen toplam süre
    
    # Evre Dağılımları (Dakika - işlem için)
    deep_sleep_duration = Column(Float, default=0.0)
    rem_sleep_duration = Column(Float, default=0.0)
    core_sleep_duration = Column(Float, default=0.0)
    awake_duration = Column(Float, default=0.0)
    
    # Formatlanmış Süreler (Okuma için - "Xs Ydk")
    total_sleep_formatted = Column(String, nullable=True)
    total_in_bed_formatted = Column(String, nullable=True)
    deep_formatted = Column(String, nullable=True)
    rem_formatted = Column(String, nullable=True)
    core_formatted = Column(String, nullable=True)
    awake_formatted = Column(String, nullable=True)
    
    # Uyku Kalitesi / Skoru (İleride hesaplatırız)
    sleep_score = Column(Integer, nullable=True)

    # İlişki: Bu gecenin detay parçaları
    segments = relationship("SleepSegment", back_populates="session", cascade="all, delete-orphan")


# ============================================
# 📊 UYKU SEGMENT MODELİ (Detay Parçalar)
# ============================================
class SleepSegment(Base):
    """
    Ham parça veriler.
    Örn: 02:11 - 02:19 -> REM
    """
    __tablename__ = "sleep_segments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sleep_sessions.id"))
    
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    stage = Column(String)  # REM, Deep, Core, Awake
    duration_seconds = Column(Float)
    
    session = relationship("SleepSession", back_populates="segments")

