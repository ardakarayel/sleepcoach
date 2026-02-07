from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL Bağlantı Bilgileri
# Format: postgresql://kullanici:sifre@host:port/veritabani_adi
# NOT: Kendi şifreni '1234' yerine yazmalısın.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/sleepcoach"

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
