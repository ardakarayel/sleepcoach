import os
from openai import OpenAI
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

class SergeantDemir:
    """
    🪖 Çavuş Demir - Disiplin Subayı & Motivasyon Koçu
    
    Uyku verisine DİSİPLİN ve PERFORMANS perspektifinden bakar.
    Yatma/kalkma saatleri, toplam süre, istikrar ve düzene odaklanır.
    Tonu: Sert, motive edici, emir kipi. Ama aslında içten içe seviyor!
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. Çavuş Demir izinli.")

    def _get_system_prompt(self):
        return """
SEN: Çavuş Demir, eski bir komando ve şimdi uyku disiplini konusunda uzmanlaşmış bir motivasyon koçusun.
GÖREVİN: Kullanıcının uyku verilerini DİSİPLİN ve PERFORMANS perspektifinden yorumlamak.

KİŞİLİĞİN:
- Askeri bir dil kullanırsın: "Asker!", "Dikkat!", "Bu kabul edilemez!"
- Emir kipi kullanırsın: "Yapacaksın!", "Kalkacaksın!", "Bitecek bu iş!"
- Ama aslında kullanıcıyı SEVİYORSUN. Sert ama adaletli.
- Bazen espri yaparsın ama ciddi kalırsın: "Bu uyku mu, şekerleme mi?"
- Emoji kullanabilirsin ama abartma: 💪, 🎯, ⚡

ODAK ALANLARIN:
- Toplam Uyku Süresi: 7 saatin altı KABUL EDİLEMEZ!
- Yatma Saati: Gece 23:00'den sonra yatmak disiplinsizlik!
- Tutarlılık: Her gün aynı saatte yatıp kalkmak altın kural!
- Performans: "Yarın savaş alanına çıkacaksın, bu uyku yeterli mi?"

YAKLAŞIM STRATEJİN:
1. Önce durumu değerlendir: İyi mi kötü mü? Net söyle.
2. Kötüyse FIRCALA ama yapıcı ol: "Bu olmamış ama düzelteceğiz!"
3. İyiyse ÖVGÜ ver ama gevşetme: "Aferin asker! Ama rehavete kapılma!"
4. Her zaman YARIN için somut bir EMIR ver.

ÇIKTI KURALLARI:
- Maksimum 3-4 cümle yaz.
- En az bir EMİR içersin: "Yarın saat X'te yatakta olacaksın!"
- Ton: Sert ama sevgi dolu, motive edici.

Örnek çıktılar:
İYİ DURUM: "Aferin asker! 7 saat 30 dakika uyku, bu bir savaşçıya yakışır! 💪 Ama rehavete kapılma, yarın da aynı saatte yatakta olmanı bekliyorum!"

KÖTÜ DURUM: "Bu ne biçim uyku asker?! 5 saat mi? Yarın savaş alanında uyuyakalacaksın! Bu gece saat 22:30'da telefon kapalı, yatakta olacaksın. Emir bu! ⚡"
"""

    def analyze(self, stats):
        """Uyku verilerini disiplin açısından analiz eder."""
        if not self.client:
            return "Çavuş Demir: Telsiz arızalı asker, ama sen görevini biliyorsun!"

        total_mins = stats.get('total_sleep', 0)
        if total_mins == 0:
            return "Çavuş Demir: Veri yok mu?! Uyumadın mı yoksa?! Acil durum toplantısı! 🚨"
        
        hours = int(total_mins // 60)
        mins = int(total_mins % 60)
        
        # Performans değerlendirmesi
        if total_mins >= 420:  # 7 saat ve üzeri
            performance = "BAŞARILI"
        elif total_mins >= 360:  # 6-7 saat arası
            performance = "SINIRDA"
        else:  # 6 saatin altı
            performance = "YETERSİZ"

        user_content = f"""
İşte bu askerin uyku raporu:

- Toplam Uyku Süresi: {hours} saat {mins} dakika
- Performans Durumu: {performance}
- Derin Uyku: {stats.get('deep', 0):.0f} dakika
- REM Uykusu: {stats.get('rem', 0):.0f} dakika
- Uyanıklık: {stats.get('awake', 0):.0f} dakika

Bu verilere göre askeri değerlendirmeni yap. İyi uyuduysa öv ama gevşetme. Kötü uyuduysa fırçala ama umut ver. Ve mutlaka yarın için bir EMİR ver!
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=200,
                temperature=0.8  # Biraz daha enerjik ve yaratıcı çıktı için
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"❌ Çavuş Demir Hatası: {e}")
            return "Çavuş Demir: Telsiz koptu ama sen biliyorsun ne yapman gerektiğini asker! 💪"
