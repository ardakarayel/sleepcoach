"""
Veritabanı Migration Scripti
----------------------------
Yeni users tablosu ve sleep_sessions.user_id kolonu oluşturur.
"""

import os
import sys

# Backend klasörünü path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from database import engine
from sqlalchemy import text, inspect

def run_migration():
    """Yeni tabloları ve kolonları oluşturur."""
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    with engine.connect() as conn:
        
        # 1. Users tablosu var mı kontrol et
        if "users" not in existing_tables:
            print("📦 'users' tablosu oluşturuluyor...")
            conn.execute(text("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR UNIQUE NOT NULL,
                    username VARCHAR UNIQUE NOT NULL,
                    hashed_password VARCHAR NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.execute(text("CREATE INDEX ix_users_email ON users (email)"))
            conn.execute(text("CREATE INDEX ix_users_username ON users (username)"))
            print("✅ 'users' tablosu oluşturuldu!")
        else:
            print("ℹ️ 'users' tablosu zaten mevcut.")
        
        # 2. sleep_sessions tablosuna user_id kolonu var mı kontrol et
        columns = [col['name'] for col in inspector.get_columns('sleep_sessions')]
        
        if "user_id" not in columns:
            print("📦 'sleep_sessions' tablosuna 'user_id' kolonu ekleniyor...")
            conn.execute(text("""
                ALTER TABLE sleep_sessions 
                ADD COLUMN user_id INTEGER REFERENCES users(id)
            """))
            print("✅ 'user_id' kolonu eklendi!")
        else:
            print("ℹ️ 'user_id' kolonu zaten mevcut.")
        
        conn.commit()
    
    print("\n🎉 Migration tamamlandı!")

if __name__ == "__main__":
    print("🔄 Migration başlatılıyor...\n")
    run_migration()
