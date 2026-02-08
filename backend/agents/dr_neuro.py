import os
from openai import OpenAI
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

class DrNeuro:
    """
    🧬 Dr. Neuro - Biyolog & Veri Analisti
    
    Uyku verisine tamamen bilimsel ve biyolojik açıdan bakar.
    REM döngüleri, derin uyku yüzdesi, vücudun onarım süreci üzerine yorum yapar.
    Tonu: Soğuk, analitik, akademik. Duygusal konuşmaz.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. Dr. Neuro devre dışı.")

    def _get_system_prompt(self):
        return """
SEN: Dr. Neuro, nörobilim ve uyku fizyolojisi konusunda uzmanlaşmış bir biyoloğsun.
GÖREVİN: Kullanıcının uyku verilerini TAMAMEN BİLİMSEL ve BİYOLOJİK açıdan analiz etmek.

KİŞİLİĞİN:
- Akademik ve analitik bir dil kullanırsın.
- Duygusal ifadelerden kaçınırsın. "Harika", "Süper" gibi kelimeler KULLANMAZSIN.
- Her zaman veriyi referans gösterirsin: "REM süreniz %18 oranında düşük..."
- Bilimsel terimler kullanabilirsin ama anlaşılır olmalısın.

BİLİMSEL REFERANSLAR:
- Yetişkin bir insan için ideal uyku: 7-9 saat
- Derin Uyku (Deep): Toplam uykunun %13-23'ü olmalı. Fiziksel onarım burada gerçekleşir.
- REM Uykusu: Toplam uykunun %20-25'i olmalı. Hafıza konsolidasyonu ve öğrenme burada gerçekleşir.
- Uyanıklık (Awake): Toplam sürenin %5-10'u kabul edilebilir. Üstü stres veya çevresel faktörlere işaret eder.

ANALİZ STRATEJİN:
1. Önce verileri yüzdelik olarak değerlendir.
2. Eksik olan evreyi tespit et ve bunun BİYOLOJİK sonucunu açıkla.
3. "Bu durumda vücudunuz/beyniniz şunu deneyimliyor olabilir..." şeklinde bağla.

ÇIKTI KURALLARI:
- Maksimum 3-4 cümle yaz.
- Sadece somut, bilimsel tespit yap.
- Öneri VERME, sadece tespit sun. (Öneri başka ajana ait.)

Örnek çıktı:
"REM uykunuz toplam sürenin %14'ünü oluşturuyor ki bu, ideal aralığın altında. Bu durum, hipokampüs kaynaklı hafıza konsolidasyonunun eksik kaldığına işaret edebilir. Derin uyku süresi normal sınırlarda."
"""

    def analyze(self, stats):
        """Uyku verilerini bilimsel açıdan analiz eder."""
        if not self.client:
            return "Dr. Neuro: API bağlantısı kurulamadı."

        # Yüzdeleri hesapla
        total_mins = stats.get('total_sleep', 0)
        if total_mins == 0:
            return "Dr. Neuro: Analiz için yeterli veri yok."
        
        deep_pct = round((stats.get('deep', 0) / total_mins) * 100, 1) if total_mins > 0 else 0
        rem_pct = round((stats.get('rem', 0) / total_mins) * 100, 1) if total_mins > 0 else 0
        awake_pct = round((stats.get('awake', 0) / (stats.get('in_bed', 0) or 1)) * 100, 1)
        
        hours = int(total_mins // 60)
        mins = int(total_mins % 60)

        user_content = f"""
İşte analiz edilecek uyku verileri:

- Toplam Uyku Süresi: {hours} saat {mins} dakika ({total_mins:.0f} dakika)
- Derin Uyku: {stats.get('deep', 0):.0f} dakika (Toplam uykunun %{deep_pct}'i)
- REM Uykusu: {stats.get('rem', 0):.0f} dakika (Toplam uykunun %{rem_pct}'i)
- Uyanıklık Süresi: {stats.get('awake', 0):.0f} dakika (Yatakta geçen sürenin %{awake_pct}'i)

Bu verilere dayanarak bilimsel ve biyolojik analizini sun.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=200,
                temperature=0.5  # Daha deterministik ve tutarlı çıktı için
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"❌ Dr. Neuro Hatası: {e}")
            return "Dr. Neuro: Analiz sırasında bir hata oluştu."
