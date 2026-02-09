import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Railway Bağlantı Adresin
DATABASE_URL = "postgresql://postgres:ttGABlfiHIrZRKPGnUhJGwWDawjyOLwx@interchange.proxy.rlwy.net:23550/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed():
    db = SessionLocal()
    print("🧹 Eski veriler temizleniyor...")
    db.execute(text("TRUNCATE sleep_segments, sleep_sessions RESTART IDENTITY CASCADE"))
    db.commit()
    
    user_id = 1
    stages = ["Deep", "REM", "Core", "Awake"]
    
    print("📅 7 günlük detaylı veri girişi başlıyor...")
    
    for i in range(7, 0, -1):
        target_date = datetime.now() - timedelta(days=i)
        # Uyku başlangıcı genelde gece 11-12 civarı
        sleep_start = target_date.replace(hour=23, minute=0, second=0, microsecond=0) + timedelta(minutes=random.randint(-30, 60))
        
        # Toplam 7-8.5 saat arası bir uyku
        total_duration_mins = random.randint(420, 510)
        current_time = sleep_start
        
        # Session Bilgileri
        stats = {"Deep": 0, "REM": 0, "Core": 0, "Awake": 0}
        segments_to_add = []
        
        # Uykuyu küçük segmentlere bölelim
        remaining_mins = total_duration_mins
        while remaining_mins > 0:
            seg_mins = min(random.randint(15, 50), remaining_mins)
            # Evreleri biraz daha gerçekçi dağıtalım (Core uykusu daha baskın)
            stage = random.choices(stages, weights=[20, 25, 45, 10])[0]
            
            seg_end = current_time + timedelta(minutes=seg_mins)
            
            segments_to_add.append({
                "st": current_time,
                "et": seg_end,
                "sg": stage,
                "ds": seg_mins * 60
            })
            
            stats[stage] += seg_mins
            current_time = seg_end
            remaining_mins -= seg_mins

        total_sleep = stats["Deep"] + stats["REM"] + stats["Core"]
        
        def fmt(m): return f"{int(m//60)}s {int(m%60)}dk"

        # 1. Session'ı Ekle
        res = db.execute(text("""
            INSERT INTO sleep_sessions (
                user_id, input_date, start_time, end_time, 
                total_sleep_duration, total_time_in_bed, 
                deep_sleep_duration, rem_sleep_duration, core_sleep_duration, awake_duration,
                total_sleep_formatted, total_in_bed_formatted, deep_formatted, rem_formatted, core_formatted, awake_formatted
            ) VALUES (:u, :id, :st, :et, :tsd, :ttb, :dsd, :rsd, :csd, :ad, :tsf, :tbf, :df, :rf, :cf, :af)
            RETURNING id
        """), {
            "u": user_id, "id": current_time, "st": sleep_start, "et": current_time,
            "tsd": total_sleep, "ttb": total_duration_mins,
            "dsd": stats["Deep"], "rsd": stats["REM"], "csd": stats["Core"], "ad": stats["Awake"],
            "tsf": fmt(total_sleep), "tbf": fmt(total_duration_mins),
            "df": fmt(stats["Deep"]), "rf": fmt(stats["REM"]), "cf": fmt(stats["Core"]), "af": fmt(stats["Awake"])
        })
        
        session_id = res.fetchone()[0]
        
        # 2. Bu Session'a ait Segmentleri Ekle
        for s in segments_to_add:
            db.execute(text("""
                INSERT INTO sleep_segments (session_id, start_time, end_time, stage, duration_seconds)
                VALUES (:sid, :st, :et, :sg, :ds)
            """), {
                "sid": session_id, "st": s["st"], "et": s["et"], "sg": s["sg"], "ds": s["ds"]
            })
            
        print(f"✅ {target_date.strftime('%d.%m')} günü uykusu ve {len(segments_to_add)} segment eklendi.")

    db.commit()
    print("\n🚀 İşlem tamam! Veritabanı pırıl pırıl ve dolu!")
    db.close()

if __name__ == "__main__":
    seed()
