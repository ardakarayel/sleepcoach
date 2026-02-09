from database import engine
from sqlalchemy import text

def add_missing_columns():
    print("🔧 Veritabanı tabloları güncelleniyor...")
    
    # Eklenecek kolonlar ve tipleri
    new_columns = [
        ("total_sleep_formatted", "VARCHAR"),
        ("total_in_bed_formatted", "VARCHAR"),
        ("deep_formatted", "VARCHAR"),
        ("rem_formatted", "VARCHAR"),
        ("core_formatted", "VARCHAR"),
        ("awake_formatted", "VARCHAR"),
    ]
    
    with engine.connect() as conn:
        for col_name, col_type in new_columns:
            try:
                # Kolon zaten var mı kontrol et (PostgreSQL için)
                print(f"🔍 {col_name} kolonu kontrol ediliyor...")
                conn.execute(text(f"ALTER TABLE sleep_sessions ADD COLUMN {col_name} {col_type}"))
                print(f"✅ {col_name} eklendi.")
            except Exception as e:
                # Kolon zaten varsa hata verir, yoksayalım
                if "already exists" in str(e) or "Duplicate column" in str(e):
                    print(f"ℹ️ {col_name} zaten mevcut.")
                else:
                    print(f"⚠️ Hata ({col_name}): {e}")
        
        conn.commit()
    
    print("🚀 Veritabanı güncellemesi tamamlandı!")

if __name__ == "__main__":
    add_missing_columns()
