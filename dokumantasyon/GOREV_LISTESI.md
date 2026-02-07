# 💤 SleepCoach MVP - Görev Takip Listesi

> MVP Dokümanına sadık kalarak hazırlanmıştır.

---

## Faz 1: Veri Kaynağı & Veri Toplama (Gün 1-5) - ✅ TAMAMLANDI

> *MVP Bölüm 4: Apple Health + Apple Watch*

- [x] **Gün 1:** Apple Health'ten veri çekme yöntemini araştır
  - [x] HealthKit / Google Fit verisine erişimi sağla (XML, API veya Webhook ile) - **iOS Shortcuts / Kestirmeler kullanıldı.**
  - [x] 2. Veri alma testini yap (Telefondan PC'ye veri aktarımı)
  - [x] 3. Gelen veriyi parse edecek (okuyacak) basit Python scripti yaz
- [x] **Gün 2:** Veri modeli tasarımı (models.py oluşturuldu)
- [x] **Gün 3:** Mock/örnek veri seti oluştur (temiz_uyku_verisi.json)
- [x] **Gün 4:** Veri depolama yapısı (PostgreSQL + SQLAlchemy)
- [x] **Gün 5:** Veri çekme mekanizmasının temel prototipi (iPhone -> Backend API)

---

## Faz 2: Backend API (Gün 6-10) - ✅ TAMAMLANDI

> *MVP Bölüm 9: Teknik Mimari*

- [x] **Gün 6:** Backend proje kurulumu (Python + FastAPI)
- [x] **Gün 7:** Veritabanı tabloları (SleepSession, SleepSegment) - **Railway Postgres Entegrasyonu yapıldı.**
- [x] **Gün 8:** Uyku verisi kaydetme endpoint'i (/upload-sleep) - **JSON Lines formatı desteklendi.**
- [x] **Gün 9:** Geçmiş veri sorgulama endpoint'leri (SQL üzerinden test edildi)
- [x] **Gün 10:** API test ve doğrulama (iPhone üzerinden başarılı kayıt alındı)

---

## Faz 3: Rule-Based Filter (Gün 11-13) - 🔜 SIRADAKİ

> *MVP Bölüm 5: Otomasyon Mantığı - "gereksiz durumlarda AI çağrılmaz"*

- [ ] **Gün 11:** Filtre kurallarını tanımla
- [ ] **Gün 12:** Rule-based filtre kodunu yaz
- [ ] **Gün 13:** Filtre testleri

---

## Faz 4: AI Agent (Gün 14-18)

> *MVP Bölüm 6: AI Agent Tasarımı*

- [ ] **Gün 14:** AI prompt tasarımı
- [ ] **Gün 15:** Pattern analizi - aynı saatlerde uyanma
- [ ] **Gün 16:** Pattern analizi - REM/Deep düşüşü, HRV
- [ ] **Gün 17:** AI çıktı formatı (max 300 token)
- [ ] **Gün 18:** AI entegrasyonu test

---

## Faz 5: Otomasyon Sistemi (Gün 19-23) - 🟡 KISMEN TAMAMLANDI

> *MVP Bölüm 5: Günlük otomatik akış*

- [ ] **Gün 19:** Scheduler kurulumu (sabah 08:00) - **iPhone Alarm Dismiss Trigger ile çözüldü.**
- [x] **Gün 20:** Günlük akış implementasyonu:
  - [x] Uyku verisi çek
  - [x] Sonucu DB'ye yaz
- [ ] **Gün 21:** Bildirim sistemi (email/push)
- [ ] **Gün 22:** "Bugün denedim" toggle mekanizması
- [ ] **Gün 23:** End-to-end otomasyon testi

---

## Faz 6: Token & Maliyet Kontrolü (Gün 24-25) - 🟡 KISMEN TAMAMLANDI

> *MVP Bölüm 7: Bilinçli sınırlamalar*

- [x] **Gün 24:** Günde 1 analiz limiti (Kotasal takip)
- [x] **Gün 25:** Token sayacı ve maliyet takibi (**Antigravity Cockpit entegre edildi.**)

---

## Faz 7: Frontend UI (Gün 26-32)

> *MVP Bölüm 8: Kullanıcı Deneyimi - "Konuşan ekran, dashboard değil"*

- [ ] **Gün 26:** Home ekranı - AI yorumu (en üstte)
- [ ] **Gün 27:** Home ekranı - 3 metrik (süre, uyanma, deep+rem %)
- [ ] **Gün 28:** Home ekranı - "Bugün denedim" toggle
- [ ] **Gün 29:** Sleep Detail ekranı
- [ ] **Gün 30:** History/Timeline ekranı
- [ ] **Gün 31:** Settings ekranı

---

## 📊 İlerleme Takibi

| Faz | Gün | Durum |
|-----|-----|-------|
| 1 - Veri Kaynağı | 1-5 | ✅ DONE |
| 2 - Backend | 6-10 | ✅ DONE |
| 3 - Rule Filter | 11-13 | ⏳ SIRADA |
| 4 - AI Agent | 14-18 | ⏳ |
| 5 - Otomasyon | 19-23 | 🟡 IN PROGRESS |
| 6 - Maliyet | 24-25 | ✅ DONE (Kotasal) |
| 7 - Frontend | 26-32 | ⏳ |

---

**Son Güncelleme:** 7 Şubat 2026
