from fastapi import FastAPI, Request, Depends, HTTPException                                         
from sqlalchemy.orm import Session
import uvicorn
import json
import dateparser
from datetime import datetime
import os

# Bağımlılıkları içe aktar
try:
    from .database import engine, Base, get_db
    from .models import SleepSession, SleepSegment
except ImportError:
    from database import engine, Base, get_db
    from models import SleepSession, SleepSegment

app = FastAPI()

# Tabloları oluştur
Base.metadata.create_all(bind=engine)

def parse_date(date_val):
    if not date_val: return None
    if isinstance(date_val, dict): date_val = date_val.get('start') or date_val.get('end')
    if isinstance(date_val, str):
        return dateparser.parse(date_val)
    return None

def clean_value(val):
    if isinstance(val, dict): return val.get('value')
    return val

def calculate_duration_from_intervals(intervals):
    if not intervals: return 0.0
    intervals.sort(key=lambda x: x[0])
    merged = []
    current_start, current_end = intervals[0]
    for next_start, next_end in intervals[1:]:
        if next_start <= current_end:
            current_end = max(current_end, next_end)
        else:
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
        return {"status": "error", "message": f"JSON Okuma Hatası: {str(e)}"}

    # --- DEDEKTİF MODU: Veriyi Bulma (GÜNCELLENDİ) ---
    raw_data = []

    # 1. Gelen şey direkt bir Liste mi?
    if isinstance(payload, list):
        raw_data = payload
    
    # 2. Gelen şey bir Sözlük (Dict) mü?
    elif isinstance(payload, dict):
        if "uyku_verisi" in payload:
            temp_data = payload["uyku_verisi"]
            # Eğer 'uyku_verisi' bir String ise, onu Listeye çevir!
            if isinstance(temp_data, str):
                try:
                    temp_data = json.loads(temp_data)
                except:
                    print("⚠️ 'uyku_verisi' string idi ama JSON'a çevrilemedi.")
            raw_data = temp_data
            
        elif "data" in payload: raw_data = payload["data"]
        elif "result" in payload: raw_data = payload["result"]
        
        # Eğer hala boşsa ve sözlük tek bir kayıt gibi duruyorsa (start/val var)
        elif "start" in payload and "value" in payload:
            raw_data = [payload]
            
        else:
            # Derin Arama: İç içe geçmiş olabilir
            for val in payload.values():
                if isinstance(val, list) and len(val) > 0:
                    raw_data = val
                    break

    # 3. Gelen şey String mi? (Bazen komple JSON string gelir)
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
            if isinstance(parsed, list): raw_data = parsed
            elif isinstance(parsed, dict) and "uyku_verisi" in parsed: raw_data = parsed["uyku_verisi"]
        except: pass

    # --- SON KONTROL ---
    if not raw_data or not isinstance(raw_data, list):
         received_type = type(payload).__name__
         received_keys = list(payload.keys()) if isinstance(payload, dict) else "Yok"
         msg = f"Geçerli veri bulunamadı. Gelen Tip: {received_type}, Anahtarlar: {received_keys}"
         print(f"❌ {msg}")
         return {"status": "error", "message": msg}

    print(f"📥 {len(raw_data)} satır veri yakalandı, hesaplanıyor...")

    # --- İŞLEME ve KAYIT (Aynı kodlar) ---
    stats = {
        "deep": 0.0, "rem": 0.0, "core": 0.0, "awake": 0.0, "in_bed": 0.0, "total_sleep": 0.0
    }
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

        if not s_time or not e_time: continue

        if min_start is None or s_time < min_start: min_start = s_time
        if max_end is None or e_time > max_end: max_end = e_time

        duration_sec = (e_time - s_time).total_seconds()
        seg = SleepSegment(
            start_time=s_time, end_time=e_time, stage=val, duration_seconds=duration_sec
        )
        segments_objects.append(seg)

        if val == "In Bed" or val == "InBed": category_intervals["InBed"].append((s_time, e_time))
        elif val == "Deep": category_intervals["Deep"].append((s_time, e_time)) 
        elif val == "REM": category_intervals["REM"].append((s_time, e_time))
        elif val == "Core": category_intervals["Core"].append((s_time, e_time))
        elif val == "Awake": category_intervals["Awake"].append((s_time, e_time))

    if not segments_objects:
        return {"status": "warning", "message": "Liste dolu ama geçerli segment yok"}

    stats["in_bed"] = calculate_duration_from_intervals(category_intervals["InBed"])
    stats["deep"] = calculate_duration_from_intervals(category_intervals["Deep"])
    stats["rem"] = calculate_duration_from_intervals(category_intervals["REM"])
    stats["core"] = calculate_duration_from_intervals(category_intervals["Core"])
    stats["awake"] = calculate_duration_from_intervals(category_intervals["Awake"])
    stats["total_sleep"] = stats["deep"] + stats["rem"] + stats["core"]

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
        segments=segments_objects
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    print(f"✅ KAYDEDİLDİ! Oturum ID: {new_session.id}")
    return {
        "status": "success",
        "session_id": new_session.id,
        "summary_minutes": stats
    }
