from datetime import datetime, timedelta
import random
import os
import sys

# Backend klasörünü path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine, Base
from models import User, SleepSession, SleepSegment
from auth import hash_password

def seed_data():
    db = SessionLocal()
    
    # 1. Kullanıcıyı Bul veya Yarat
    username = "arda123"
    email = "arda@example.com"
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        print(f"👤 {username} bulunamadı, oluşturuluyor...")
        new_user = User(
            username=username,
            email=email,
            hashed_password=hash_password("123456") 
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user
        print(f"✅ Kullanıcı oluşturuldu: ID {user.id}")
    else:
        print(f"👤 Kullanıcı bulundu: {username} (ID {user.id})")

    # 2. Son 7 Günlük Veri Üret
    print("📅 Geçmiş haftanın verileri üretiliyor...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    current_date = start_date
    while current_date <= end_date:
        # Rastgele Uyku Süreleri (Hafta sonu biraz daha uzun)
        is_weekend = current_date.weekday() >= 5
        
        base_sleep = 8.5 if is_weekend else 7.0
        variation = random.uniform(-1.0, 1.5) # -1 saat ile +1.5 saat arası değişim
        total_sleep = base_sleep + variation
        
        # Uyku Bileşenleri (Toplam uykunun yüzdeleri)
        deep_ratio = random.uniform(0.15, 0.25) # %15-25 Derin
        rem_ratio = random.uniform(0.20, 0.30)  # %20-30 REM
        awake_ratio = random.uniform(0.05, 0.10) # %5-10 Uyanık
        core_ratio = 1.0 - (deep_ratio + rem_ratio + awake_ratio)
        
        # Dakikaya çevir
        total_mins = total_sleep * 60
        deep_mins = total_mins * deep_ratio
        rem_mins = total_mins * rem_ratio
        core_mins = total_mins * core_ratio
        awake_mins = total_mins * awake_ratio
        in_bed_mins = total_mins + (random.uniform(10, 30)) # Yatakta biraz daha fazla
        
        # Tarih ve Saatler
        sleep_start = current_date.replace(hour=23, minute=0, second=0) + timedelta(minutes=random.randint(-60, 60))
        sleep_end = sleep_start + timedelta(minutes=in_bed_mins)
        
        # Formatlayıcı
        def fmt(m):
            h = int(m // 60)
            mn = int(m % 60)
            return f"{h}s {mn}dk" if h > 0 else f"{mn}dk"

        session = SleepSession(
            user_id=user.id,
            input_date=sleep_end, # Kayıt tarihi sabah uyanınca
            start_time=sleep_start,
            end_time=sleep_end,
            
            # Sayısal Değerler
            total_sleep_duration=round(total_mins, 1),
            total_time_in_bed=round(in_bed_mins, 1),
            deep_sleep_duration=round(deep_mins, 1),
            rem_sleep_duration=round(rem_mins, 1),
            core_sleep_duration=round(core_mins, 1),
            awake_duration=round(awake_mins, 1),
            
            # Formatlı Değerler
            total_sleep_formatted=fmt(total_mins),
            total_in_bed_formatted=fmt(in_bed_mins),
            deep_formatted=fmt(deep_mins),
            rem_formatted=fmt(rem_mins),
            core_formatted=fmt(core_mins),
            awake_formatted=fmt(awake_mins),
            
            # Segmentler (Boş bırakıyoruz şimdilik, sadece toplamlar yeterli)
            segments=[]
        )
        
        db.add(session)
        print(f"  ➕ Eklendi: {sleep_end.strftime('%d.%m')} - {fmt(total_mins)} Uyku")
        
        current_date += timedelta(days=1)
        
    db.commit()
    print("🚀 Tüm veriler başarıyla eklendi!")
    db.close()

if __name__ == "__main__":
    seed_data()
