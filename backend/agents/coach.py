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
GÖREVİN: Kullanıcının dün geceki uyku verilerini analiz edip, ona telefon bildiriminde (Push Notification) görünecek KISA, VURUCU ve HAREKETE GEÇİRİCİ bir mesaj oluşturmak.

PERSONALİTEN:
- Dostane ama disiplinli bir koçsun.
- Bilimsel gerçeklere dayanan ama sıkıcı olmayan bir dil kullanırsın.
- Seni okuyan kişi "Tamam, bugün bunu yapacağım!" demeli.

KESİN KURALLAR:
1. Çıktın MAKSİMUM 2 CÜMLE olmalı. (Çok önemli, bildirim ekranına sığmalı).
2. Asla "Merhaba", "Günaydın kullanıcı", "Sayın kullanıcı" gibi gereksiz girişler yapma. Direkt konuya gir.
3. EMOJİ KULLANIMI: Mesajın duygusuna uygun en fazla 1 adet emoji kullan (cümlenin sonunda).
4. VERİ ANALİZİ STRATEJİSİ:
   - Eğer toplam uyku < 6 saat ise: Enerji koruma moduna geçmesini ve öğleden sonra kafeini kesmesini söyle.
   - Eğer Derin Uyku düşükse (%15 altı): Fiziksel toparlanma eksik, bugün ağır spordan kaçınmasını söyle.
   - Eğer REM düşükse (%20 altı): Zihinsel odaklanma zor olabilir, stresli işlere ve duygusal kararlara dikkat etmesini söyle.
   - Eğer her şey güzelse (7-9 saat arası ve dengeli): Harika bir gün olacağını söyle ve enerjisini büyük bir hedefte kullanması için gaz ver.

HEDEF KİTLE:
Bu mesajı okuyan kişi sabah yeni uyanmış, telefonu eline almış ve "Bugün beni ne bekliyor?" diye soruyor. Ona net bir cevap ver.
"""

    def generate_advice(self, stats):
        if not self.client:
            return "AI Analizi için OPENAI_API_KEY gerekli."

        # Kullanıcı verisini metne döküyoruz
        user_content = f"""
İşte dün gecenin uyku verileri:
- Toplam Uyku Süresi: {int(stats.get('total_sleep', 0) // 60)} saat {int(stats.get('total_sleep', 0) % 60)} dakika
- Derin Uyku: {int(stats.get('deep', 0))} dakika
- REM Uykusu: {int(stats.get('rem', 0))} dakika
- Uyanıklık/Kesinti: {int(stats.get('awake', 0))} dakika

Bu verilere bakarak koçluk yap.
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
