import os
from openai import OpenAI
from dotenv import load_dotenv

# Çevresel değişkenleri yükle (.env varsa)
load_dotenv()

class SleepCoach:
    def __init__(self):
        # API Key kontrolü
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. Yapay zeka devre dışı.")

    def _get_system_prompt(self):
        return """
SEN: SleepCoach uygulamasının yapay zeka tabanlı "Uyku Koçu"sun.
GÖREVİN: Kullanıcının uyku verilerini analiz edip, ona telefon bildiriminde (Push Notification) görünecek KISA, VURUCU ve SKOR ODAKLI bir mesaj oluşturmak.

PERSONALİTEN:
- Dostane ama disiplinli bir koçsun.
- Sayısal skorları yorumun içine doğal bir şekilde yedirirsin.
- Seni okuyan kişi "Tamam, bugün nasıl hissedeceğimi anladım!" demeli.

KESİN KURALLAR:
1. Çıktın MAKSİMUM 15 KELİME olmalı. (Çok kısa ve net).
2. Mesajın BAŞINDA mutlaka skoru belirt: "⭐ Skor: X/100 | ..."
3. Asla "Merhaba" deme. Direkt analizi patlat: "Enerjin düşük, bugün sakin..."
4. VERİ ANALİZİ STRATEJİSİ VE SKOR YORUMU:
   - Skor < 70 ve Toplam < 6 saat: Enerji tasarrufu modu. Öğleden sonra kafeini kes.
   - Skor > 70 ama Derin Düşük: Fiziksel toparlanma eksik, spora dikkat.
   - Skor > 70 ama REM Düşük: Zihinsel olarak dağınık olabilirsin, stresten kaçın.
   - Skor > 85: Harika bir gün! Enerjini büyük hedeflere sakla.

Bu mesajı okuyan kişi sabah yeni uyanmış, telefonu eline almış ve "Bugün beni ne bekliyor?" diye soruyor. Ona net bir cevap ver.
"""

    def generate_advice(self, stats):
        if not self.client:
            return "AI Analizi için OPENAI_API_KEY gerekli."

        # Basit Skor Hesabı (Backend tarafında da yapılabilir ama burada da olsun)
        total_mins = stats.get('total_sleep', 0)
        score = min(100, max(0, int((total_mins / 480) * 100))) # 8 saat referans

        # Kullanıcı verisini metne döküyoruz
        user_content = f"""
İşte dün gecenin uyku verileri:
- HESAPLANAN SKOR: {score} / 100
- Toplam Uyku Süresi: {int(total_mins // 60)} saat {int(total_mins % 60)} dakika
- Derin Uyku: {int(stats.get('deep', 0))} dakika
- REM Uykusu: {int(stats.get('rem', 0))} dakika
- Uyanıklık: {int(stats.get('awake', 0))} dakika

Bu skora ve veriye göre bildirim mesajını oluştur.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Daha stabil ve ucuz model
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=100,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"❌ OpenAI Hatası: {e}")
            return "Koç şu an analiz yapamıyor, ama uykunu kaydettim."
