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

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS AYARLARI (Ön Yüzden Gelen İstekleri Kabul Et) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için ileride sadece domain'e kısıtlanabilir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def format_duration(minutes):
    """Dakikayı 'Xs Ydk' formatına çevirir. Örn: 356.3 -> '5s 56dk'"""
    if minutes is None or minutes == 0:
        return "0dk"
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    if hours > 0:
        return f"{hours}s {mins}dk"
    return f"{mins}dk"

# --- REKÜRSİF VERİ BULUCU (İNATÇI DEDEKTİF) ---
def find_valid_sleep_list(obj):
    """
    Verilen objenin içinde (ne kadar derinde olursa olsun)
    uyku verisi listesini bulmaya çalışır.
    JSON Lines formatını da destekler (satır satır JSON).
    """
    # 1. Eğer bu bir listeyse ve içinde uyku verisi varsa (start/value)
    if isinstance(obj, list):
        if len(obj) > 0 and isinstance(obj[0], dict):
            if 'start' in obj[0] or 'value' in obj[0] or 'startDate' in obj[0]:
                return obj
        for item in obj:
            res = find_valid_sleep_list(item)
            if res: return res
    
    # 2. Eğer bu bir sözlükse, değerlerini tara
    elif isinstance(obj, dict):
        for key in ['uyku_verisi', 'data', 'result', 'body', 'value']:
            if key in obj:
                res = find_valid_sleep_list(obj[key])
                if res: return res
        for val in obj.values():
            res = find_valid_sleep_list(val)
            if res: return res

    # 3. Eğer bu bir string ise
    elif isinstance(obj, str):
        obj_stripped = obj.strip()
        
        # 3a. Normal JSON Array mı? [...]
        if obj_stripped.startswith('['):
            try:
                parsed = json.loads(obj_stripped)
                return find_valid_sleep_list(parsed)
            except:
                pass
        
        # 3b. JSON Lines formatı mı? (Her satır ayrı bir JSON objesi)
        elif '\n' in obj_stripped or obj_stripped.startswith('{'):
            lines = obj_stripped.split('\n')
            parsed_list = []
            for line in lines:
                line = line.strip()
                if line and line.startswith('{'):
                    try:
                        parsed_list.append(json.loads(line))
                    except:
                        pass
            if parsed_list:
                print(f"🔄 JSON Lines formatı algılandı, {len(parsed_list)} satır parse edildi.")
                return parsed_list
            
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

    stats["in_bed"] = round(calculate_duration_from_intervals(category_intervals["InBed"]), 1)
    stats["deep"] = round(calculate_duration_from_intervals(category_intervals["Deep"]), 1)
    stats["rem"] = round(calculate_duration_from_intervals(category_intervals["REM"]), 1)
    stats["core"] = round(calculate_duration_from_intervals(category_intervals["Core"]), 1)
    stats["awake"] = round(calculate_duration_from_intervals(category_intervals["Awake"]), 1)
    stats["total_sleep"] = round(stats["deep"] + stats["rem"] + stats["core"], 1)

    new_session = SleepSession(
        input_date=datetime.now(),
        start_time=min_start,
        end_time=max_end,
        # Sayısal değerler (işlem için)
        total_sleep_duration=stats["total_sleep"],
        total_time_in_bed=stats["in_bed"],
        deep_sleep_duration=stats["deep"],
        rem_sleep_duration=stats["rem"],
        core_sleep_duration=stats["core"],
        awake_duration=stats["awake"],
        # Formatlanmış değerler (okuma için)
        total_sleep_formatted=format_duration(stats["total_sleep"]),
        total_in_bed_formatted=format_duration(stats["in_bed"]),
        deep_formatted=format_duration(stats["deep"]),
        rem_formatted=format_duration(stats["rem"]),
        core_formatted=format_duration(stats["core"]),
        awake_formatted=format_duration(stats["awake"]),
        segments=segments_objects
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    print(f"✅ KAYDEDİLDİ! Oturum ID: {new_session.id}")
    
    # --- UYKU KONSEYİ (AI AGENTS) ---
    ai_advice = None
    try:
        # Import Yolu Düzeltmesi (Railway vs Local)
        try:
            from agents.supervisor import Supervisor
        except ImportError:
            from backend.agents.supervisor import Supervisor
            
        # Konseyi başlat
        council = Supervisor()
        
        print("🏛️ Uyku Konseyi toplanıyor...")
        ai_advice = council.generate_council_report(stats)
        print(f"📋 Konsey Raporu: {ai_advice}")
        
    except Exception as e:
        print(f"⚠️ Konsey Hatası: {str(e)}")
        import traceback
        traceback.print_exc()
        ai_advice = "Konsey şu an toplanamadı, ama verilerin güvende."

    return {
        "status": "success",
        "session_id": new_session.id,
        "summary_minutes": stats,
        "ai_advice": ai_advice
    }

@app.get("/latest-sleep")
def get_latest_sleep(db: Session = Depends(get_db)):
    """
    En son kaydedilen uyku oturumunu getirir.
    Ek olarak 'Navigation' (önceki/sonraki) verisini de döner.
    """
    latest_session = db.query(SleepSession).order_by(SleepSession.input_date.desc()).first()
    
    if not latest_session:
        return {"status": "empty", "message": "Henüz veri yok."}
    
    # Navigation: Sadece önceki kayıt olabilir (Son zaten bu)
    prev_session = db.query(SleepSession).filter(SleepSession.input_date < latest_session.input_date).order_by(SleepSession.input_date.desc()).first()
    
    return prepare_session_response(latest_session, prev_session=prev_session, next_session=None)

@app.get("/sleep/{session_id}")
def get_sleep_by_id(session_id: int, db: Session = Depends(get_db)):
    """
    Belirli bir ID'ye sahip uyku oturumunu getirir.
    Sağa/Sola geçişler için kullanılır.
    """
    current_session = db.query(SleepSession).filter(SleepSession.id == session_id).first()
    
    if not current_session:
        return {"status": "error", "message": "Kayıt bulunamadı."}
        
    # Önceki Kayıt (Tarihi daha eski olan en yakın kayıt)
    prev_session = db.query(SleepSession).filter(SleepSession.input_date < current_session.input_date).order_by(SleepSession.input_date.desc()).first()
    
    # Sonraki Kayıt (Tarihi daha yeni olan en yakın kayıt)
    next_session = db.query(SleepSession).filter(SleepSession.input_date > current_session.input_date).order_by(SleepSession.input_date.asc()).first()
    
    return prepare_session_response(current_session, prev_session, next_session)

def prepare_session_response(session, prev_session=None, next_session=None):
    """Ortak response hazırlayıcı"""
    stats = {
        "total_sleep": session.total_sleep_duration,
        "deep": session.deep_sleep_duration,
        "rem": session.rem_sleep_duration,
        "core": session.core_sleep_duration,
        "awake": session.awake_duration,
        "in_bed": session.total_time_in_bed
    }
    
    formatted = {
        "total": session.total_sleep_formatted,
        "deep": session.deep_formatted,
        "rem": session.rem_formatted,
        "awake": session.awake_formatted,
        "date": session.input_date.strftime("%d.%m.%Y %H:%M")
    }

    return {
        "status": "success",
        "data": {
            "stats": stats,
            "formatted": formatted,
            "session_id": session.id
        },
        "navigation": {
            "prev_id": prev_session.id if prev_session else None,
            "next_id": next_session.id if next_session else None
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Sunucu Port {port} üzerinde başlatılıyor...")
    uvicorn.run(app, host="0.0.0.0", port=port)
