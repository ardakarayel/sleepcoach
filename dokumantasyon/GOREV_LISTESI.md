# 💤 SleepCoach MVP - Görev Takip Listesi

> MVP Dokümanına sadık kalarak hazırlanmıştır.

---

## Faz 1: Veri Kaynağı & Veri Toplama (Gün 1-5)

> *MVP Bölüm 4: Apple Health + Apple Watch*

- [ ] **Gün 1:** Apple Health'ten veri çekme yöntemini araştır
  - iOS companion app mi?
  - CSV export/import mı?
  - [x] 1. HealthKit / Google Fit verisine erişimi sağla (XML, API veya Webhook ile)
  - [x] 2. Veri alma testini yap (Telefondan PC'ye veri aktarımı)
  - [x] 3. Gelen veriyi parse edecek (okuyacak) basit Python scripti yaz
- [ ] **Gün 2:** Veri modeli tasarımı
  - Uyku başlangıç/bitiş
  - Uyku evreleri (REM, Deep, Core, Awake)
  - Uyanma sayısı
  - Kalp atış hızı, HRV
- [ ] **Gün 3:** Mock/örnek veri seti oluştur (test için)
- [ ] **Gün 4:** Veri depolama yapısı (veritabanı şeması)
- [ ] **Gün 5:** Veri çekme mekanizmasının temel prototipi

---

## Faz 2: Backend API (Gün 6-10)

> *MVP Bölüm 9: Teknik Mimari*

- [ ] **Gün 6:** Backend proje kurulumu (Python + FastAPI)
- [ ] **Gün 7:** Veritabanı tabloları (Users, SleepData, Insights)
- [ ] **Gün 8:** Uyku verisi kaydetme endpoint'i
- [ ] **Gün 9:** Geçmiş veri sorgulama endpoint'leri
- [ ] **Gün 10:** API test ve doğrulama

---

## Faz 3: Rule-Based Filter (Gün 11-13)

> *MVP Bölüm 5: Otomasyon Mantığı - "gereksiz durumlarda AI çağrılmaz"*

- [ ] **Gün 11:** Filtre kurallarını tanımla
  - AI çağır: Uyanma > 2, Deep < %10, pattern var
  - AI çağırma: Her şey normal
- [ ] **Gün 12:** Rule-based filtre kodunu yaz
- [ ] **Gün 13:** Filtre testleri

---

## Faz 4: AI Agent (Gün 14-18)

> *MVP Bölüm 6: AI Agent Tasarımı*

- [ ] **Gün 14:** AI prompt tasarımı
  - Son 1 gece + son 7/14 gün verisini oku
  - Tek ana problem seç
  - Tek aksiyon öner
- [ ] **Gün 15:** Pattern analizi - aynı saatlerde uyanma
- [ ] **Gün 16:** Pattern analizi - REM/Deep düşüşü, HRV
- [ ] **Gün 17:** AI çıktı formatı (max 300 token)
  - 1 kısa yorum
  - 1 sebep
  - 1 aksiyon
  - 1 takip cümlesi
- [ ] **Gün 18:** AI entegrasyonu test

---

## Faz 5: Otomasyon Sistemi (Gün 19-23)

> *MVP Bölüm 5: Günlük otomatik akış*

- [ ] **Gün 19:** Scheduler kurulumu (sabah 08:00)
- [ ] **Gün 20:** Günlük akış implementasyonu:
  - Uyku verisi çek
  - Geçmiş ile birleştir
  - Filtre uygula
  - Gerekirse AI çağır
  - Sonucu DB'ye yaz
- [ ] **Gün 21:** Bildirim sistemi (email/push)
- [ ] **Gün 22:** "Bugün denedim" toggle mekanizması
- [ ] **Gün 23:** End-to-end otomasyon testi

---

## Faz 6: Token & Maliyet Kontrolü (Gün 24-25)

> *MVP Bölüm 7: Bilinçli sınırlamalar*

- [ ] **Gün 24:** Günde 1 analiz limiti
- [ ] **Gün 25:** Token sayacı ve maliyet takibi

---

## Faz 7: Frontend UI (Gün 26-32)

> *MVP Bölüm 8: Kullanıcı Deneyimi - "Konuşan ekran, dashboard değil"*

- [ ] **Gün 26:** Home ekranı - AI yorumu (en üstte)
- [ ] **Gün 27:** Home ekranı - 3 metrik (süre, uyanma, deep+rem %)
- [ ] **Gün 28:** Home ekranı - "Bugün denedim" toggle
- [ ] **Gün 29:** Sleep Detail ekranı
- [ ] **Gün 30:** History/Timeline ekranı
- [ ] **Gün 31:** Settings ekranı
- [ ] **Gün 32:** UI polish ve son testler

---

## 📊 İlerleme Takibi

| Faz | Gün | Durum |
|-----|-----|-------|
| 1 - Veri Kaynağı | 1-5 | ⏳ |
| 2 - Backend | 6-10 | ⏳ |
| 3 - Rule Filter | 11-13 | ⏳ |
| 4 - AI Agent | 14-18 | ⏳ |
| 5 - Otomasyon | 19-23 | ⏳ |
| 6 - Maliyet | 24-25 | ⏳ |
| 7 - Frontend | 26-32 | ⏳ |

---

**Son Güncelleme:** 6 Şubat 2026
