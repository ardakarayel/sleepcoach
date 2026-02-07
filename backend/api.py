from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn
import json
import dateparser
from datetime import datetime

# Bağımlılıkları içe aktar (Hem modül hem script olarak çalışmaya uygun)
try:
    from .database import engine, Base, get_db
    from .models import SleepSession, SleepSegment
except ImportError:
    from database import engine, Base, get_db
    from models import SleepSession, SleepSegment

app = FastAPI()

# Tabloları oluştur (eğer yoksa garanti olsun)
Base.metadata.create_all(bind=engine)

def parse_date(date_val):
    """Tarih verisini güvenli şekilde datetime objesine çevirir"""
    if not date_val: return None
    if isinstance(date_val, dict): date_val = date_val.get('start') or date_val.get('end')
    
    if isinstance(date_val, str):
        return dateparser.parse(date_val)
    return None

def clean_value(val):
    """Değer verisini temizler"""
    if isinstance(val, dict): return val.get('value')
    return val

def calculate_duration_from_intervals(intervals):
    """
    Çakışan zaman aralıklarını birleştirir ve toplam süreyi dk olarak hesaplar.
    Örnek: (00:00-08:00) ve (01:00-07:00) -> Toplam 8 saat
    """
    if not intervals: return 0.0
    
    # Başlangıç zamanına göre sırala
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    current_start, current_end = intervals[0]
    
    for next_start, next_end in intervals[1:]:
        if next_start <= current_end: # Çakışma var, süreyi uzat
            current_end = max(current_end, next_end)
        else: # Çakışma bitti, yeni blok ekle
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
    
    merged.append((current_start, current_end))
    
    total_minutes = 0.0
    for s, e in merged:
        total_minutes += (e - s).total_seconds() / 60.0
        
    return total_minutes

@app.post("/upload-sleep")
async def receive_sleep_data(request: Request, db: Session = Depends(get_db)):
    try:
        payload = await request.json()
    except Exception as e:
        return {"status": "error", "message": f"JSON Hatası: {str(e)}"}

    # --- Veri Çıkarma ve Temizleme ---
    raw_data = []
    if isinstance(payload, dict):
        if "uyku_verisi" in payload:
            raw_data = payload["uyku_verisi"]
        else:
            raw_data = [payload]
    elif isinstance(payload, list):
        raw_data = payload
    
    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except: pass 

    if not raw_data or not isinstance(raw_data, list):
         return {"status": "error", "message": "Geçerli veri bulunamadı"}

    print(f"📥 {len(raw_data)} satır veri alındı, OTOMASYON işlemi başlıyor...")

    # --- Yedekleme (Opsiyonel ama güvenli) ---
    try:
        with open("son_gelen_veri.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=4, ensure_ascii=False)
    except: pass

    # --- İstatistik Değişkenleri ---
    stats = {
        "deep": 0.0, "rem": 0.0, "core": 0.0, "awake": 0.0, "in_bed": 0.0, "total_sleep": 0.0
    }
    
    # Aralık listeleri (Akıllı hesaplama için)
    category_intervals = {
        "Deep": [], "REM": [], "Core": [], "Awake": [], "InBed": [], "Asleep": []
    }

    segments_objects = []
    min_start = None
    max_end = None

    for item in raw_data:
        s_time = parse_date(item.get('start'))
        e_time = parse_date(item.get('end'))
        val = clean_value(item.get('value'))

        if not s_time or not e_time:
            continue

        # Global zaman sınırları
        if min_start is None or s_time < min_start: min_start = s_time
        if max_end is None or e_time > max_end: max_end = e_time

        # Segment Oluştur
        duration_sec = (e_time - s_time).total_seconds()
        
        seg = SleepSegment(
            start_time=s_time,
            end_time=e_time,
            stage=val,
            duration_seconds=duration_sec
        )
        segments_objects.append(seg)

        # Aralıkları Sınıflandır
        if val == "In Bed" or val == "InBed":
            category_intervals["InBed"].append((s_time, e_time))
        elif val == "Deep":
            category_intervals["Deep"].append((s_time, e_time)) 
        elif val == "REM":
            category_intervals["REM"].append((s_time, e_time))
        elif val == "Core":
            category_intervals["Core"].append((s_time, e_time))
        elif val == "Awake":
            category_intervals["Awake"].append((s_time, e_time))

    if not segments_objects:
        return {"status": "warning", "message": "Hiçbir segment işlenemedi"}

    # --- HESAPLAMA (Akıllı Birleştirme) ---
    stats["in_bed"] = calculate_duration_from_intervals(category_intervals["InBed"])
    stats["deep"] = calculate_duration_from_intervals(category_intervals["Deep"])
    stats["rem"] = calculate_duration_from_intervals(category_intervals["REM"])
    stats["core"] = calculate_duration_from_intervals(category_intervals["Core"])
    stats["awake"] = calculate_duration_from_intervals(category_intervals["Awake"])
    
    # Toplam Uyku = Deep + REM + Core
    stats["total_sleep"] = stats["deep"] + stats["rem"] + stats["core"]

    # --- Veritabanı Kaydı ---
    new_session = SleepSession(
        input_date=datetime.now(),
        start_time=min_start,
        end_time=max_end,
        total_sleep_duration=stats["total_sleep"],
        total_time_in_bed=stats["in_bed"],
        deep_sleep_duration=stats["deep"],
        rem_sleep_duration=stats["rem"],
        core_sleep_duration=stats["core"],
        awake_duration=stats["awake"],
        segments=segments_objects # Detayları da ekle
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    print(f"✅ KAYDEDİLDİ! Oturum ID: {new_session.id}")
    print(f"💤 Toplam: {int(stats['total_sleep'])} dk | 🛌 Yatakta: {int(stats['in_bed'])} dk")
    print("--------------------------------------------------")

    return {
        "status": "success",
        "session_id": new_session.id,
        "summary_minutes": stats
    }

if __name__ == "__main__":
    print("🚀 Tam Otomatik Uyku Sunucusu Hazır: http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
