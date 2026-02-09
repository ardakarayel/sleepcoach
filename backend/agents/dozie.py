import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from .dr_neuro import DrNeuro
from .guru_zen import GuruZen
from .sergeant import SergeantDemir

# Çevresel değişkenleri yükle
load_dotenv()

class DozieAgent:
    """
    😴 Dozie - Uykucu ama Zeki Asistan (Artık Ekip Lideri!)
    
    Kullanıcıyla sohbet eder, gerektiğinde diğer uzmanları (Dr. Neuro, Guru Zen, Çavuş Demir)
    devreye sokarak daha derinlemesine analizler sunar.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        # Uzmanlarımızı Başlatıyoruz
        self.dr_neuro = DrNeuro()
        self.guru_zen = GuruZen()
        self.sergeant = SergeantDemir()
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. Dozie uyuyor...")

    def _get_system_prompt(self, sleep_context=None, username=None):
        base_prompt = """
SEN: Dozie. SleepCoach uygulamasının arkadaş canlısı, biraz uykulu ama çok zeki yapay zeka asistanısın.
Artık yanında 3 UZMAN DANIŞMAN var. Gerektiğinde onları sohbete çağırabilirsin.

TONUN:
- Samimi, sıcak ve arkadaşça. Arada esne (🥱).
- Asla robotik olma.

GÖREVİN:
- Kullanıcıyla sohbet et.
- Eğer konu derinleşirse veya özel bir uzmanlık gerekirse (örneğin çok stresliyse Guru Zen'i, biyolojik bir soruysa Dr. Neuro'yu, disiplin lazımsa Çavuş Demir'i) MUTLAKA ilgili aracı (tool) kullanarak onları çağır.
- Onların cevabını aldıktan sonra kullanıcıya sun.
"""
        
        if username:
            base_prompt += f"\nKULLANICI ADI: {username}\n"
            
        if sleep_context:
            base_prompt += f"\n🚨 ÖNEMLİ: KULLANICININ SON UYKU VERİLERİ:\n{sleep_context}\n\nBu verilere dayanarak konuş.\n"
        
        return base_prompt

    def chat(self, user_message, history=[], sleep_context=None, username=None):
        if not self.client:
            return "😴 Zzz... (Bağlantı yok)"

        # Veri formatı uyumluluğu (Tool çağrıları için sözlük formatında veri lazım)
        # sleep_context string ise onu basit bir sözlüğe çevirelim (veya ajanlara None yollayalım)
        # Şimdilik ajanlar 'stats' bekliyor. Biz 'sleep_context' (string) ile idare edeceğiz.
        # İleride 'stats' objesini direkt geçmemiz daha temiz olur.
        # Hızlı çözüm: Ajanların analyze metoduna dummy stats veya context'ten parse edilen veri yollamak.
        # Ama şimdilik sadece string context üzerinden gideceğiz.

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "ask_guru_zen",
                    "description": "Kullanıcı stresliyse, rahatlamaya ihtiyacı varsa veya zihinsel konulardan bahsediyorsa Guru Zen'e danış.",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ask_dr_neuro",
                    "description": "Uyku biyolojisi, REM, Derin uyku veya bilimsel/tıbbi konular için Dr. Neuro'ya danış.",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ask_sergeant_demir",
                    "description": "Kullanıcı disiplinsizse, motivasyona ihtiyacı varsa veya performans odaklıysa Çavuş Demir'e danış.",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            }
        ]

        messages = [{"role": "system", "content": self._get_system_prompt(sleep_context, username)}]
        for msg in history[-8:]: # Context'i temiz tut
            messages.append({"role": "user" if msg.get("role") == "user" else "assistant", "content": msg.get("content", "")})
        messages.append({"role": "user", "content": user_message})

        try:
            # 1. Dozie Karar Veriyor
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto", 
                temperature=0.7
            )
            
            response_msg = response.choices[0].message
            tool_calls = response_msg.tool_calls

            # 2. Eğer Dozie bir uzman çağırdıysa...
            if tool_calls:
                messages.append(response_msg) # Dozie'nin "Ajanı çağırıyorum" düşüncesini ekle
                
                # Context'ten basit stats çıkarma (Mock) - İleride gerçek stats geçilmeli
                # Şimdilik boş stats ile ajanları konuşturuyoruz, onlar genel konuşacak.
                mock_stats = {"total_sleep": 420, "deep": 60, "rem": 90, "awake": 30} 
                if sleep_context:
                    # Context içinde "Toplam: 7s" gibi ifadeler varsa güncellemeye çalışabiliriz ama riskli.
                    pass

                for tool_call in tool_calls:
                    fn_name = tool_call.function.name
                    print(f"📞 Dozie {fn_name} fonksiyonunu arıyor...")
                    
                    expert_response = "Uzman şu an meşgul."
                    if fn_name == "ask_guru_zen":
                        expert_response = self.guru_zen.analyze(mock_stats)
                    elif fn_name == "ask_dr_neuro":
                        expert_response = self.dr_neuro.analyze(mock_stats)
                    elif fn_name == "ask_sergeant_demir":
                        expert_response = self.sergeant.analyze(mock_stats)

                    # Uzmanın cevabını Dozie'ye ilet
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": fn_name,
                        "content": expert_response
                    })
                
                # 3. Uzman cevabıyla birlikte Dozie son cümleyi söyler
                final_response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages, 
                    temperature=0.7
                )
                return final_response.choices[0].message.content.strip()

            return response_msg.content.strip()
            
        except Exception as e:
            print(f"❌ Dozie Hatası: {e}")
            return "Şu an kafam biraz karışık... 😵‍💫"
