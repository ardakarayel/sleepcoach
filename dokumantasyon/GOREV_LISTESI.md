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
| 5 - Otomasyon | 19-23 | ✅ DONE |
| 6 - Maliyet | 24-25 | ✅ DONE (Kotasal) |
| 7 - Frontend | 26-32 | ✅ DONE (MVP Dashboard) |

---

**Son Güncelleme:** 7 Şubat 2026

## 🚀 Gelecek Vizyonu & İş Fikri Backlog
Bu liste, MVP sonrası projeyi bir girişime (Start-up) dönüştürmek için saklanmaktadır.

- [ ] **SaaS Dönüşümü:** Çoklu kullanıcı desteği (Multi-tenancy) ile arkadaşlara link atıp davet etme.
- [ ] **Aile Planı (Gamification):** Eşler veya aile üyeleri arasında "Kim daha iyi uyudu?" liderlik tablosu.
- [ ] **Kişiselleştirilmiş Koçluk:** 
  - Sporcu profili -> "Protein al, kas onarımı eksik."
  - Beyaz yakalı profili -> "Geç saatte mail bakma, REM düşüyor."

---

## Faz 8: Kullanıcı Kimlik Doğrulama (Authentication) - 🚧 AKTİF

> *Kullanıcı hesabı sistemi - Sign In / Sign Up*

### 📋 Şimdi Yapılacaklar (Öncelikli)
- [ ] **Backend:** User modeli oluştur (email, username, password)
- [ ] **Backend:** /register endpoint'i (Kayıt)
- [ ] **Backend:** /login endpoint'i (Giriş) - JWT Token döner
- [ ] **Backend:** sleep_sessions tablosuna user_id kolonu ekle
- [ ] **Frontend:** Login sayfası (/login)
- [ ] **Frontend:** Register sayfası (/register)
- [ ] **Frontend:** Koruma: Giriş yapmadan ana sayfaya erişim engellenir
- [ ] **AI Ajanlar:** Username ile kişiselleştirilmiş selamlama

### 📝 İleri Tarihte Yapılacaklar (Backlog)
- [ ] **Email Doğrulama:** Kayıt sonrası "Email'ini doğrula" linki gönder
- [ ] **Beni Hatırla:** Uzun süreli token seçeneği (30 gün)
- [ ] **Şifremi Unuttum:** Email'e şifre sıfırlama linki gönder
- [ ] **Google/Apple ile Giriş:** OAuth entegrasyonu

---

## Faz 9: Uyku Konseyi (AI Multi-Agent) - ✅ TAMAMLANDI

> *3 uzman ajan + Supervisor sistemi*

- [x] **Dr. Neuro:** Biyolojik/bilimsel analiz ajanı
- [x] **Guru Zen:** Zihinsel sağlık ve rahatlama koçu
- [x] **Çavuş Demir:** Disiplin subayı ve motivasyon koçu
- [x] **Supervisor (Başkan):** 3 raporun sentezi + aksiyon planı

---

## Faz 10: Frontend Login UI - 🚧 PLANLAMASI TAMAMLANDI

> *"Gece Gökyüzü" temalı premium giriş deneyimi*

### 🎨 Tasarım Konsepti
- **Tema:** Koyu mavi → mor gradyan arka plan
- **Gece Animasyonu:** Yıldızlar titreşiyor, ay fazları değişiyor
- **Glassmorphism:** Buzlu cam efekti form kartlarında
- **Micro-interactions:** Butonlarda, inputlarda yumuşak hover efektleri

### 📱 Sayfa Akışı (3 Kaydırmalı Ekran)
| Sayfa | İçerik | Animasyon |
|-------|--------|-----------|
| 1. Hoş Geldin | Ay + "SleepCoach" logosu + slogan | Ay yavaşça dolunay oluyor |
| 2. Giriş Yap | Email + Şifre formu + "Kayıt ol" linki | Sağdan sola kayarak giriyor |
| 3. Kayıt Ol | Email + Username + Şifre formu | Sağdan sola kayarak giriyor |

### 🎭 Animasyonlar (Framer Motion)
| Animasyon | Nerede | Detay |
|-----------|--------|-------|
| Yıldız Titreşimi | Arka plan | Rastgele pozisyonlarda yıldızlar parlaması |
| Ay Fazları | Hoş geldin ekranı | Hilal → Dolunay geçişi (3 saniye) |
| Sayfa Geçişi | Login ↔ Register | Sağdan sola kayma + fade |
| Form Girişi | Input focus | Hafif scale + glow efekti |
| Buton Hover | Tüm butonlar | Gradient renk kayması + scale |

### 🌈 Renk Paleti
| Renk | Kullanım | Kod |
|------|----------|-----|
| Gece Mavisi | Arka plan | `#0a0a1a` → `#1a1a3a` |
| Mor Vurgu | Butonlar, linkler | `#8b5cf6` |
| Ay Altın | Ay, vurgu noktaları | `#fbbf24` |
| Beyaz/Gri | Metinler | `#ffffff`, `#9ca3af` |
| Cam Efekti | Form kartları | `rgba(255,255,255,0.05)` + blur |

### ⏰ Dinamik Selamlama (Saat Bazlı)
| Saat Aralığı | Mesaj |
|--------------|-------|
| 05:00 - 12:00 | "Günaydın, {username}! ☀️" |
| 12:00 - 18:00 | "İyi günler, {username}! 🌤️" |
| 18:00 - 22:00 | "İyi akşamlar, {username}! 🌅" |
| 22:00 - 05:00 | "İyi geceler, {username}! 🌙" |

### 🔐 Oturum Yönetimi
- **Token Saklama:** localStorage (7 gün geçerli token)
- **Otomatik Giriş:** Sayfa açılınca token var mı kontrol, varsa direkt dashboard'a
- **Çıkış:** Settings sayfasında "Çıkış Yap" butonu

### 🛠️ Teknik Stack
- Next.js 14 (mevcut)
- Framer Motion (sayfa geçişleri, animasyonlar)
- Tailwind CSS (glassmorphism, gradyanlar)
- localStorage (token saklama)

### 📋 Yapılacaklar Listesi
- [ ] Framer Motion kur
- [ ] Layout + Gece teması arka plan
- [ ] Hoş Geldin sayfası (Ay animasyonu)
- [ ] Login sayfası (Glassmorphism form)
- [ ] Register sayfası
- [ ] Sayfa geçiş animasyonları
- [ ] Token saklama + Otomatik giriş
- [ ] Dinamik selamlama (saat bazlı)
- [ ] Yıldız animasyonu (arka plan)

### 🌟 Bonus Fikirler (İleri Tarih)
- [ ] Uyku Skoru ile Arka Plan (Skor düşük → bulutlu, Skor yüksek → yıldızlı)
- [ ] Ses Efektleri (Login başarılı olunca yumuşak "ding")
- [ ] Haptic Feedback (Mobilde titreşim - PWA)

---

**Son Güncelleme:** 8 Şubat 2026 (21:03)

