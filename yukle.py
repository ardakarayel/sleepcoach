import json
from datetime import datetime
import dateparser
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from backend.models import SleepSession, SleepSegment
from backend.database import SessionLocal, engine

# Veritabanı bağlantısı
db = SessionLocal()

FILE_PATH = "temiz_uyku_verisi.json"

def clean_value(val):
    if isinstance(val, dict): return val.get('value')
    return val

def parse_date(date_val):
    if not date_val: return None
    if isinstance(date_val, dict): date_val = date_val.get('start') or date_val.get('end')
    if isinstance(date_val, str):
        return dateparser.parse(date_val)
    return None

def temizlik_yap():
    """Önceki hatalı kayıtları temizler"""
    try:
        db.execute(text("TRUNCATE TABLE sleep_sessions CASCADE"))
        db.commit()
        print("🧹 Eski kayıtlar temizlendi.")
    except Exception as e:
        print(f"⚠️ Temizlik hatası: {e}")
        db.rollback()

def calculate_duration_from_intervals(intervals):
    """
    Çakışan zaman aralıklarını birleştirir ve toplam süreyi hesaplar.
    Örnek: (00:00-08:00) ve (01:00-07:00) -> Toplam 8 saat (üst üste binmeleri eler)
    """
    if not intervals: return 0.0
    
    # Başlangıç zamanına göre sırala
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    current_start, current_end = intervals[0]
    
    for next_start, next_end in intervals[1:]:
        if next_start <= current_end: # Çakışma var
            current_end = max(current_end, next_end)
        else: # Çakışma bitti, yeni blok
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
    
    merged.append((current_start, current_end))
    
    total_minutes = 0.0
    for s, e in merged:
        total_minutes += (e - s).total_seconds() / 60.0
        
    return total_minutes

def yukle():
    temizlik_yap()
    
    print(f"📂 '{FILE_PATH}' dosyası okunuyor...")
    
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("❌ Dosya bulunamadı!")
        return

    # İstatistik Değişkenleri
    stats = {
        "deep": 0.0, "rem": 0.0, "core": 0.0, "awake": 0.0, "in_bed": 0.0, "total_sleep": 0.0
    }
    
    # Aralıkları (Intervals) toplamak için listeler
    category_intervals = {
        "Deep": [], "REM": [], "Core": [], "Awake": [], "InBed": [], "Asleep": []
    }
    
    segments_objects = []
    min_start = None
    max_end = None

    print(f"📊 {len(raw_data)} satır veri analiz ediliyor...")

    for item in raw_data:
        s_time = parse_date(item.get('start'))
        e_time = parse_date(item.get('end'))
        val = clean_value(item.get('value'))

        if not s_time or not e_time: continue

        # Zaman sınırlarını bul
        if min_start is None or s_time < min_start: min_start = s_time
        if max_end is None or e_time > max_end: max_end = e_time
        
        # Segment objesi oluştur
        duration_sec = (e_time - s_time).total_seconds()
        
        seg = SleepSegment(
            start_time=s_time,
            end_time=e_time,
            stage=val,
            duration_seconds=duration_sec
        )
        segments_objects.append(seg)

        # Aralıkları listeye ekle (Hesaplama için)
        if val == "In Bed" or val == "InBed":
            category_intervals["InBed"].append((s_time, e_time))
        elif val in category_intervals:
            category_intervals[val].append((s_time, e_time))

    if not segments_objects:
        print("⚠️ Hiçbir geçerli segment bulunamadı.")
        return

    # --- HESAPLAMA (Akıllı Birleştirme) ---
    # Tüm kategoriler için overlap (çakışma) kontrolü yaparak süre hesapla
    stats["in_bed"] = calculate_duration_from_intervals(category_intervals["InBed"])
    stats["deep"] = calculate_duration_from_intervals(category_intervals["Deep"])
    stats["rem"] = calculate_duration_from_intervals(category_intervals["REM"])
    stats["core"] = calculate_duration_from_intervals(category_intervals["Core"])
    stats["awake"] = calculate_duration_from_intervals(category_intervals["Awake"])
    
    # Toplam Uyku = Deep + REM + Core 
    # (Not: Asleep verisini yine kullanmıyoruz, detayları topluyoruz)
    stats["total_sleep"] = stats["deep"] + stats["rem"] + stats["core"]

    # Oturum Oluştur
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
    
    print("\n✅ BAŞARILI! Veritabanına Yüklendi.")
    print("--------------------------------------------------")
    print(f"🆔 Oturum ID: {new_session.id}")
    
    t_sleep = int(stats['total_sleep'])
    print(f"💤 Toplam Uyku: {t_sleep} dk ({int(t_sleep//60)} sa {int(t_sleep%60)} dk)")
    
    t_bed = int(stats['in_bed'])
    print(f"🛌 Yatakta: {t_bed} dk ({int(t_bed//60)} sa {int(t_bed%60)} dk)")
    
    print(f"🧠 REM: {int(stats['rem'])} dk | 🌊 Derin: {int(stats['deep'])} dk | ⚙️ Core: {int(stats['core'])} dk")
    print(f"👁️ Uyanık: {int(stats['awake'])} dk")
    print("--------------------------------------------------")

if __name__ == "__main__":
    yukle()
