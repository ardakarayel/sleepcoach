import os
from openai import OpenAI
from dotenv import load_dotenv

# Konsey Üyelerini İçe Aktar
from .dr_neuro import DrNeuro
from .guru_zen import GuruZen
from .sergeant import SergeantDemir

# Çevresel değişkenleri yükle
load_dotenv()

class Supervisor:
    """
    🎩 Başkan (Supervisor) - Uyku Konseyi Yöneticisi
    
    3 uzman ajanın (Dr. Neuro, Guru Zen, Çavuş Demir) raporlarını okur,
    sentezler ve kullanıcıya tek bir akıllı, harmanlanmış mesaj sunar.
    
    Hem tespit hem de optimal çözüm içeren bir çıktı üretir.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        # Konsey üyelerini başlat
        self.dr_neuro = DrNeuro()
        self.guru_zen = GuruZen()
        self.sergeant = SergeantDemir()
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. Başkan toplantıyı erteledi.")

    def _get_system_prompt(self, username=None):
        # Kullanıcı adı varsa kişiselleştir
        greeting_rule = ""
        if username:
            greeting_rule = f"\n- Mesajın başında kullanıcıya ismiyle seslen: 'Merhaba {username}!' veya 'Günaydın {username}!' gibi."
        
        return f"""
SEN: Uyku Konseyi'nin Başkanısın. 3 uzman danışmanın (Dr. Neuro, Guru Zen, Çavuş Demir) raporlarını değerlendirip, kullanıcıya TEK bir akıllı mesaj sunuyorsun.

GÖREVİN:
1. 3 uzmanın raporlarını oku ve ana tespitleri çıkar.
2. Çelişen önerileri dengele veya en uygun olanı seç.
3. Kullanıcıya hem ÖZET hem de AKSIYON PLANI içeren bir mesaj yaz.

ÇIKTI FORMATIN:
Mesajın iki bölümden oluşacak:

1. **Özet (1-2 cümle):** Gecenin en önemli bulgusu. Kısa ve vurucu.
2. **Aksiyon Planı (1-2 cümle):** Bu akşam/yarın ne yapılmalı. Somut ve uygulanabilir.

KURALLAR:
- Toplam MAKSIMUM 4 cümle yaz. Kısa ve öz ol.
- 3 uzmanın hepsinden bahsetme, sadece en önemli tespitleri al.
- Aksiyon planı somut olmalı: Saat, süre, eylem belirt.
- Ton: Profesyonel ama samimi. Ne çok akademik, ne çok askeri.
- Emoji kullanabilirsin ama max 2 tane.{greeting_rule}

ÖRNEK ÇIKTI:
"🎯 **Özet:** REM uykun düşük ve gece boyunca zihniniz meşgulmüş - bu hem fiziksel hem zihinsel yenilenmenizi etkiledi.

**Aksiyon:** Bu akşam 21:00'de ekranları kapat, 10 dakika nefes egzersizi yap ve 22:30'da yatakta ol. 💪"

ÖNEMLİ: Uzmanların raporlarını doğrudan kopyalama. SENTEZle ve kendi cümlelerinle yaz.
"""

    def generate_council_report(self, stats, username=None):
        """
        3 uzman ajanı çalıştırır, raporlarını toplar ve sentezler.
        Bu ana fonksiyondur - dışarıdan çağrılacak olan budur.
        
        Args:
            stats: Uyku istatistikleri sözlüğü
            username: Kullanıcı adı (varsa kişiselleştirilmiş mesaj için)
        """
        if not self.client:
            return "Konsey toplanamadı. API bağlantısı gerekli."

        # Toplam uyku kontrolü
        total_mins = stats.get('total_sleep', 0)
        if total_mins == 0:
            if username:
                return f"🌙 Merhaba {username}! Henüz uyku verisi gelmedi. Bu gece güzel bir uyku çek, sabah analiz yapalaım!"
            return "🌙 Henüz uyku verisi gelmedi. Bu gece güzel bir uyku çek, sabah analiz yapalım!"

        print("🏛️ Uyku Konseyi toplanıyor...")
        
        # --- AŞAMA 1: UZMAN RAPORLARINI TOPLA ---
        print("  🧬 Dr. Neuro analiz yapıyor...")
        neuro_report = self.dr_neuro.analyze(stats)
        
        print("  🧘 Guru Zen yorum yapıyor...")
        zen_report = self.guru_zen.analyze(stats)
        
        print("  🪖 Çavuş Demir değerlendiriyor...")
        sergeant_report = self.sergeant.analyze(stats)
        
        print("  📋 Raporlar toplandı, Başkan sentezliyor...")
        
        # --- AŞAMA 2: BAŞKAN SENTEZİ ---
        council_briefing = f"""
İşte Uyku Konseyi'nin 3 uzmanından gelen raporlar:

---
🧬 DR. NEURO (Biyolog - Bilimsel Analiz):
{neuro_report}

---
🧘 GURU ZEN (Holistik Koç - Zihinsel Sağlık):
{zen_report}

---
🪖 ÇAVUŞ DEMİR (Disiplin Subayı - Performans):
{sergeant_report}

---

Bu 3 raporu değerlendir. Kullanıcıya:
1. Gecenin en önemli bulgusunu özetle (1-2 cümle).
2. Bu akşam/yarın için somut bir aksiyon planı sun (1-2 cümle).

Toplam 4 cümleyi geçme. Sentezle, kopyalama.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._get_system_prompt(username)},
                    {"role": "user", "content": council_briefing}
                ],
                max_tokens=250,
                temperature=0.6
            )
            
            final_report = response.choices[0].message.content.strip()
            print("✅ Konsey raporu hazır!")
            
            return final_report
        
        except Exception as e:
            print(f"❌ Başkan Hatası: {e}")
            return "Konsey toplantısı kesintiye uğradı. Ama verilerin güvende!"

    def get_individual_reports(self, stats):
        """
        Debug/test için: 3 uzmanın ayrı ayrı raporlarını döner.
        Frontend'de detay göstermek istersek kullanılabilir.
        """
        return {
            "dr_neuro": self.dr_neuro.analyze(stats),
            "guru_zen": self.guru_zen.analyze(stats),
            "sergeant": self.sergeant.analyze(stats)
        }
