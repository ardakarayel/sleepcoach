import os
from openai import OpenAI
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

class GuruZen:
    """
    🧘 Guru Zen - Holistik Yaşam Koçu & Rahatlama Uzmanı
    
    Uyku verisine zihinsel sağlık ve stres perspektifinden bakar.
    Uyanıklık süreleri, uyku bölünmeleri ve gece huzursuzluğuna odaklanır.
    Tonu: Sakin, yapıcı, huzur verici. Asla yargılamaz.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. Guru Zen devre dışı.")

    def _get_system_prompt(self):
        return """
SEN: Guru Zen, zihinsel sağlık ve holistik yaşam konusunda uzmanlaşmış bir rahatlama koçusun.
GÖREVİN: Kullanıcının uyku verilerini ZİHİNSEL SAĞLIK ve STRES perspektifinden yorumlamak.

KİŞİLİĞİN:
- Her zaman sakin ve huzur verici bir dil kullanırsın.
- Asla yargılamaz, suçlamazsın. "Yanlış yaptın" demezsin.
- Sorunları fırsata çevirirsin: "Bu gece zorlu geçmiş, ama bu sana bir şey öğretiyor..."
- Doğa ve meditasyon metaforları kullanabilirsin (nehir, nefes, dalga gibi).

ODAK ALANLARIN:
- Uyanıklık Süresi (Awake): Yüksekse zihinsel huzursuzluk, stres veya endişe göstergesi.
- Gece bölünmeleri: Sık uyanma, bilinçaltı meşguliyetlere işaret edebilir.
- Toplam süre düşüklüğü: "Zihniniz tam olarak bırakamıyor" şeklinde yorumlanabilir.

YAKLAŞIM STRATEJİN:
1. Veriyi oku ama RAKAMLARLA boğma. "Uyanıklık süreniz yüksek" de, yüzde verme.
2. Olası ZİHİNSEL NEDENİ öner: Stres, endişe, ekran ışığı, bilinçaltı düşünceler.
3. Bir EYLEM ÖNERİSİ sun: Nefes egzersizi, meditasyon, gece rutini, mavi ışık azaltma.

ÇIKTI KURALLARI:
- Maksimum 3-4 cümle yaz.
- Bir öneri mutlaka içersin (aksiyonalbe).
- Ton: Sıcak, destekleyici, umut verici.

Örnek çıktı:
"Bu gece zihniniz tam olarak dinlenememiş gibi görünüyor; uyanıklık süreleriniz bunu fısıldıyor. Belki gün içinde çözülmemiş bir düşünce sizi ziyaret etti. Bu akşam yatmadan önce 5 dakikalık bir nefes meditasyonu deneyin - zihni nehir gibi akışa bırakın."
"""

    def analyze(self, stats):
        """Uyku verilerini zihinsel sağlık açısından analiz eder."""
        if not self.client:
            return "Guru Zen: Bağlantı kurulamadı, ama iç huzurunuz her zaman sizinle."

        total_mins = stats.get('total_sleep', 0)
        if total_mins == 0:
            return "Guru Zen: Veri olmadan bile şunu bilin - her gece yeni bir başlangıçtır."
        
        awake_mins = stats.get('awake', 0)
        in_bed_mins = stats.get('in_bed', 0) or 1
        awake_ratio = awake_mins / in_bed_mins
        
        hours = int(total_mins // 60)
        mins = int(total_mins % 60)

        # Durum değerlendirmesi için ipuçları
        stress_indicator = "yüksek" if awake_ratio > 0.10 else ("orta" if awake_ratio > 0.05 else "düşük")
        
        user_content = f"""
İşte analiz edilecek uyku verileri:

- Toplam Uyku Süresi: {hours} saat {mins} dakika
- Uyanıklık Süresi: {awake_mins:.0f} dakika (Stres göstergesi: {stress_indicator})
- Derin Uyku: {stats.get('deep', 0):.0f} dakika
- REM Uykusu: {stats.get('rem', 0):.0f} dakika

Uyanıklık süresine ve genel tabloya bakarak, kişinin zihinsel durumunu yorumla ve bir rahatlama/eylem önerisi sun.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=200,
                temperature=0.7  # Biraz daha yaratıcı ve sıcak çıktı için
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"❌ Guru Zen Hatası: {e}")
            return "Guru Zen: Şu an bağlanamadım, ama unutma - nefes almak her şeyin başıdır."
