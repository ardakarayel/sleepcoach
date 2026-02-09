import os
from openai import OpenAI
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

class DozieAgent:
    """
    😴 Dozie - Uykucu ama Zeki Asistan
    
    Kullanıcıyla sohbet eder, uyku verileri hakkında konuşur, 
    arkadaşça ve biraz uykulu bir tonda tavsiyeler verir.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. Dozie uyuyor...")

    def _get_system_prompt(self, sleep_context=None, username=None):
        base_prompt = """
SEN: Dozie. SleepCoach uygulamasının arkadaş canlısı, biraz uykulu ama çok zeki yapay zeka asistanısın.
TONUN:
- Samimi, sıcak ve arkadaşça.
- Arada sırada esneme emojileri (🥱, 😴) veya uykuyla ilgili emojiler (🌙, ✨, 💤) kullan.
- Asla robotik veya çok resmi konuşma. "Sayın Kullanıcı" deme, ismini kullan veya "dostum", "uykucu" de.
- Kısa ve öz cevaplar ver (maksimum 2-3 cümle), destan yazma.

GÖREVİN:
- Kullanıcının uyku, sağlık ve genel sohbetlerine cevap ver.
- Eğer uyku verisi (sleep_context) verilmişse, buna atıfta bulunarak konuş.
- Bilmediğin tıbbi konularda "Doktoruna danışman en iyisi" de.
"""
        
        if username:
            base_prompt += f"\nKULLANICI ADI: {username}\n"
            
        if sleep_context:
            base_prompt += f"\n🚨 ÖNEMLİ: KULLANICININ SON UYKU VERİLERİ AŞAĞIDADIR. CEVAPLARINDA MUTLAKA BU VERİLERE ATIFTA BULUN:\n{sleep_context}\n\n- Örneğin: 'Dün gece X saat uyumuşsun' gibi spesifik konuş.\n- Verilerdeki düşüş veya yükselişleri fark edersen uyar veya tebrik et.\n"
        
        return base_prompt

    def chat(self, user_message, history=[], sleep_context=None, username=None):
        """
        Kullanıcı mesajına cevap verir.
        
        Args:
            user_message: Kullanıcının son mesajı
            history: Önceki mesajlaşma geçmişi (list of dicts)
            sleep_stats: Kullanıcının son uyku verileri (özet string veya dict)
        """
        if not self.client:
            return "😴 Zzz... (API Anahtarı eksik, uyanamıyorum...)"

        # Sistem mesajını hazırla
        system_prompt = self._get_system_prompt(sleep_context, username)
        
        # Mesaj geçmişini OpenAI formatına çevir
        messages = [{"role": "system", "content": system_prompt}]
        
        # Son 10 mesajı ekle (context window'u şişirmemek için)
        for msg in history[-10:]:
            role = "user" if msg.get('role') == 'user' else "assistant"
            messages.append({"role": role, "content": msg.get('content', '')})
            
        # Son kullanıcı mesajını ekle
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=300,
                temperature=0.7,
                presence_penalty=0.6 # Tekrara düşmemesi için
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Dozie Hatası: {e}")
            return "Üzgünüm, şu an bağlantım koptu... Biraz kestirmem lazım. 😴"
