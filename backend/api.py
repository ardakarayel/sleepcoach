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

# --- REKÜRSİF VERİ BULUCU (İNATÇI DEDEKTİF) ---
def find_valid_sleep_list(obj):
    """
    Verilen objenin içinde (ne kadar derinde olursa olsun)
    uyku verisi listesini bulmaya çalışır.
    """
    # 1. Eğer bu bir listeyse ve içinde uyku verisi varsa (start/value)
    if isinstance(obj, list):
        if len(obj) > 0 and isinstance(obj[0], dict):
            # Basit kontrol: içinde 'start' veya 'value' anahtarı var mı?
            if 'start' in obj[0] or 'value' in obj[0] or 'startDate' in obj[0]:
                return obj
        # Liste ama içi boş veya başka bir şey, belki listenin içinde başka bir yapı vardır?
        for item in obj:
            res = find_valid_sleep_list(item)
            if res: return res
    
    # 2. Eğer bu bir sözlükse, değerlerini tara
    elif isinstance(obj, dict):
        # Öncelikli anahtarlar
        for key in ['uyku_verisi', 'data', 'result', 'body', 'value']:
            if key in obj:
                res = find_valid_sleep_list(obj[key])
                if res: return res
        
        # Diğer tüm değerler
        for val in obj.values():
            res = find_valid_sleep_list(val)
            if res: return res

    # 3. Eğer bu bir string ise, JSON olarak açmayı dene
    elif isinstance(obj, str):
        try:
            if obj.strip().startswith('[') or obj.strip().startswith('{'):
                parsed = json.loads(obj)
                return find_valid_sleep_list(parsed)
        except:
            pass
            
    return None

@app.post("/upload-sleep")
async def receive_sleep_data(request: Request, db: Session = Depends(get_db)):
    try:
        payload = await request.json()
    except Exception as e:
        return {"status": "error", "message": f"JSON Okuma Hatası: {str(e)}"}

    # --- İNATÇI DEDEKTİF İŞ BAŞINDA ---
    print(f"🔍 Veri aranıyor... Gelen Tip: {type(payload)}")
    raw_data = find_valid_sleep_list(payload)

    # --- KONTROL ---
    if not raw_data:
         received_keys = list(payload.keys()) if isinstance(payload, dict) else "Yok"
         msg = f"Geçerli veri bulunamadı. Gelen Anahtarlar: {received_keys}"
         print(f"❌ {msg}")
         
         # Debug için loga yazdıralım (kısa hali)
         print(f"DEBUG PAYLOAD: {str(payload)[:200]}...")
         
         return {"status": "error", "message": msg}

    print(f"📥 {len(raw_data)} satır geçerli veri bulundu! İşleniyor...")

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
        s_time = parse_date(item.get('start') or item.get('startDate'))
        e_time = parse_date(item.get('end') or item.get('endDate'))
        val = clean_value(item.get('value'))

        if not s_time or not e_time: continue

        if min_start is None or s_time < min_start: min_start = s_time
        if max_end is None or e_time > max_end: max_end = e_time

        duration_sec = (e_time - s_time).total_seconds()
        
        # Safe string conversion for stage
        stage_val = str(val) if val is not None else "Unknown"

        seg = SleepSegment(
            start_time=s_time, end_time=e_time, stage=stage_val, duration_seconds=duration_sec
        )
        segments_objects.append(seg)

        if stage_val in ["In Bed", "InBed", "ASLEEP_UNSPECIFIED"]: category_intervals["InBed"].append((s_time, e_time))
        elif "Deep" in stage_val: category_intervals["Deep"].append((s_time, e_time)) 
        elif "REM" in stage_val: category_intervals["REM"].append((s_time, e_time))
        elif "Core" in stage_val: category_intervals["Core"].append((s_time, e_time))
        elif "Awake" in stage_val: category_intervals["Awake"].append((s_time, e_time))

    if not segments_objects:
        return {"status": "warning", "message": "Liste dolu ama geçerli segment yok (Tarih formatı sorunu olabilir)"}

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Sunucu Port {port} üzerinde başlatılıyor...")
    uvicorn.run(app, host="0.0.0.0", port=port)
