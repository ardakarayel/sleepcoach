import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL Bağlantı Bilgileri
# 1. Önce Railway'in verdiği DATABASE_URL'e bak
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Eğer yoksa (yani yerel bilgisayardaysak), yerel veritabanını kullan
if not SQLALCHEMY_DATABASE_URL:
    # NOT: Eğer yerelde şifren farklıysa, burayı '1234' yerine güncelle
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/sleepcoach"

# Railway bazen "postgres://" verir ama SQLAlchemy "postgresql://" ister. Bunu düzeltelim.
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (FastAPI endpointlerinde kullanmak için)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
