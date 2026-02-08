"""
Uyku Konseyi Test Scripti
-------------------------
Bu script, 3 uzman ajanı ve Supervisor'ı test eder.
Gerçek API çağrısı yapar, bu yüzden OPENAI_API_KEY gerekli.
"""

import os
import sys

# Backend klasörünü path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Test verisi (örnek bir gece)
test_stats = {
    "total_sleep": 356,   # 5 saat 56 dakika (düşük)
    "deep": 45,           # 45 dakika derin uyku
    "rem": 52,            # 52 dakika REM
    "core": 259,          # Geri kalan core
    "awake": 38,          # 38 dakika uyanık
    "in_bed": 420         # 7 saat yatakta
}

def test_individual_agents():
    """Her bir ajanı ayrı ayrı test eder."""
    print("\n" + "="*60)
    print("🧪 BİREYSEL AJAN TESTLERİ")
    print("="*60)
    
    from agents.dr_neuro import DrNeuro
    from agents.guru_zen import GuruZen
    from agents.sergeant import SergeantDemir
    
    print("\n🧬 DR. NEURO ANALİZİ:")
    print("-" * 40)
    dr = DrNeuro()
    print(dr.analyze(test_stats))
    
    print("\n🧘 GURU ZEN YORUMU:")
    print("-" * 40)
    zen = GuruZen()
    print(zen.analyze(test_stats))
    
    print("\n🪖 ÇAVUŞ DEMİR DEĞERLENDİRMESİ:")
    print("-" * 40)
    sgt = SergeantDemir()
    print(sgt.analyze(test_stats))

def test_supervisor():
    """Supervisor'ı test eder - tüm konsey toplanır."""
    print("\n" + "="*60)
    print("🏛️ UYKU KONSEYİ TOPLANTISI")
    print("="*60)
    
    from agents.supervisor import Supervisor
    
    council = Supervisor()
    report = council.generate_council_report(test_stats)
    
    print("\n📋 BAŞKAN RAPORU (FİNAL):")
    print("-" * 40)
    print(report)

if __name__ == "__main__":
    print("\n🌙 UYKU KONSEYİ TEST SİSTEMİ 🌙")
    print("Test verisi: 5 saat 56 dakika uyku (düşük performans)")
    
    # API Key kontrolü
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ HATA: OPENAI_API_KEY bulunamadı!")
        print("   .env dosyasına API key'inizi ekleyin.")
        sys.exit(1)
    
    print("\n✅ API Key bulundu, testler başlıyor...\n")
    
    # Testleri çalıştır
    test_individual_agents()
    test_supervisor()
    
    print("\n" + "="*60)
    print("✅ TÜM TESTLER TAMAMLANDI!")
    print("="*60 + "\n")
