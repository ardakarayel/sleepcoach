from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class SleepSession(Base):
    __tablename__ = "sleep_sessions"

    id = Column(Integer, primary_key=True, index=True)
    input_date = Column(DateTime, index=True)  # Verinin sisteme girdiği tarih
    
    # Oturumun genel sınırları
    start_time = Column(DateTime) # Uyku başlangıcı
    end_time = Column(DateTime)   # Uyanış
    
    # Özet Veriler (Dakika cinsinden tutalım)
    total_sleep_duration = Column(Float, default=0.0) # Sadece uyunan (Deep+REM+Core)
    total_time_in_bed = Column(Float, default=0.0)    # Yatakta geçen toplam süre
    
    # Evre Dağılımları (Dakika)
    deep_sleep_duration = Column(Float, default=0.0)
    rem_sleep_duration = Column(Float, default=0.0)
    core_sleep_duration = Column(Float, default=0.0)
    awake_duration = Column(Float, default=0.0)
    
    # Uyku Kalitesi / Skoru (İleride hesaplatırız)
    sleep_score = Column(Integer, nullable=True)

    # İlişki: Bu gecenin detay parçaları
    segments = relationship("SleepSegment", back_populates="session", cascade="all, delete-orphan")

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
