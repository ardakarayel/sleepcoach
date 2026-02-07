# 💤 SleepCoach MVP - Detaylı Uygulama Planı

> MVP Dokümanına sadık kalınarak hazırlanmıştır.
> Frontend en sonda yapılacaktır.

---

## 🎯 Tek Cümlelik Ürün Tanımı
*"Bu uygulama uykunu ölçmez, uykunu anlamaya çalışır."*

---

## FAZ 1: Veri Kaynağı (Gün 1-5)

### Amaç
Apple Health'ten çekilecek verileri tanımlamak ve veri akışını kurmak.

### Çekilecek Veriler (MVP Bölüm 4)
| Veri | Açıklama |
|------|----------|
| Uyku başlangıç/bitiş | Yatış ve kalkış saati |
| Uyku evreleri | REM, Deep, Core, Awake süreleri |
| Uyanma sayısı | Gece kaç kez uyandı |
| Kalp atış hızı | Uyku sırasındaki ortalama |
| HRV | Kalp ritmi değişkenliği |

### Veri Erişim Seçenekleri
| Yöntem | Açıklama |
|--------|----------|
| iOS HealthKit | Doğrudan API (iOS app gerekir) |
| CSV Export | Manuel export/import |
| Alternatif cihaz | Garmin/Fitbit API |

---

## FAZ 2: Backend API (Gün 6-10)

### Veritabanı Şeması

```sql
-- Kullanıcılar
users (id, device_id, created_at, settings)

-- Uyku verileri
sleep_sessions (
  id, user_id, date,
  start_time, end_time, total_duration,
  deep_min, rem_min, core_min, awake_min,
  avg_hr, hrv, wake_count
)

-- AI yorumları
insights (
  id, user_id, date,
  comment, reason, action, followup,
  tokens_used, created_at
)

-- Kullanıcı aksiyonları
user_actions (id, insight_id, tried, feedback)
```

### API Endpoints
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | /api/sleep | Uyku verisi kaydet |
| GET | /api/sleep/history | Geçmiş veriler |
| GET | /api/insight/today | Bugünkü AI yorumu |
| POST | /api/action | "Bugün denedim" |

---

## FAZ 3: Rule-Based Filter (Gün 11-13)

### Amaç (MVP Bölüm 5)
"Gereksiz durumlarda AI çağrılmaz"

### Kurallar
**AI Çağır:**
- Uyanma sayısı > 2
- Deep sleep < %10
- Son 3 gün aynı saatte uyanma

**AI Çağırma:**
- Her şey normal aralıkta
- Bugün zaten analiz yapıldı

---

## FAZ 4: AI Agent (Gün 14-18)

### Agent Görevi (MVP Bölüm 6)
1. Son 1 gece + son 7/14 gün verisini oku
2. Pattern ara
3. **Tek** ana problem seç
4. **Tek** aksiyon öner

### Aranacak Pattern'ler
- Aynı saatlerde uyanma
- REM/Deep düşüşü
- HRV değişimi

### AI Çıktı Formatı (max 300 token)
```
1 kısa yorum
1 sebep
1 aksiyon
1 takip cümlesi
```

### Örnek Ton (MVP'den)
> "Son 4 gecedir aynı saatte uyanıyorsun.
> Bu tesadüf değil.
> Bugün yatmadan 2 saat önce yemek yememeyi deneyelim.
> Yarın sonucu birlikte kontrol edeceğiz."

---

## FAZ 5: Otomasyon (Gün 19-23)

### Günlük Otomatik Akış (MVP Bölüm 5)
```
1. Sabah 08:00
2. Son gecenin uyku verisi çekilir
3. Backend geçmiş verilerle birleştirir
4. Gerekirse AI agent çalışır
5. Sonuç DB'ye yazılır
6. Kullanıcı app'i açtığında sonucu görür
```

### Kullanıcı Etkileşimi
- Pasif (sadece okur)
- İsterse "Bugün denedim" toggle

---

## FAZ 6: Token & Maliyet (Gün 24-25)

### Bilinçli Sınırlamalar (MVP Bölüm 7)
| Limit | Değer |
|-------|-------|
| Günlük analiz | 1 kullanıcı başına |
| Max input token | ~1500 |
| Max output token | ~300 |

### Tahmini Maliyet
| Kullanıcı | Aylık |
|-----------|-------|
| 1 kişi | $0.5-1 |
| 100 kişi | $20-60 |

---

## FAZ 7: Frontend UI (Gün 26-32)

### Prensip (MVP Bölüm 8)
❌ Dashboard
✅ Konuşan ekran

### 4 Ekran

**1️⃣ Home**
- En üstte AI yorumu
- 3 metrik: Süre, Uyanma, Deep+REM %
- "Bugün denedim" toggle

**2️⃣ Sleep Detail**
- Basit grafik
- "Bu gece neden bölündü?" açıklama

**3️⃣ History/Timeline**
- Gün gün: AI ne dedi, ne denendi, sonuç

**4️⃣ Settings**
- Veri izinleri
- Günlük analiz açık/kapalı

---

## 🎯 Başarı Kriterleri (MVP Bölüm 10)

- [ ] Kullanıcı "Evet, bu beni gerçekten anlıyor" diyor
- [ ] 1 hafta kullandıktan sonra "fark ettim" tepkisi
- [ ] "Bunu geliştiririm" hissi

---

## ❌ MVP Dışında (Bölüm 11)

- Medikal teşhis
- Çoklu sensör
- Sosyal özellikler
- Premium plan

---

**Son Güncelleme:** 6 Şubat 2026
