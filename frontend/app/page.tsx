'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from './contexts/AuthContext';
import StarryBackground from './components/StarryBackground';

// Tip tanımları
interface SleepData {
  stats: {
    total_sleep: number;
    deep: number;
    rem: number;
    awake: number;
    in_bed: number;
  };
  formatted: {
    total: string;
    deep: string;
    rem: string;
    awake: string;
    date: string;
  };
}

interface Navigation {
  prev_id: number | null;
  next_id: number | null;
}

export default function Home() {
  const [data, setData] = useState<SleepData | null>(null);
  const [nav, setNav] = useState<Navigation>({ prev_id: null, next_id: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { user, token, isLoading: authLoading, getGreeting, logout } = useAuth();
  const router = useRouter();

  // 🔐 Auth Kontrolü - Giriş yapmamışsa /auth'a yönlendir
  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/auth');
    }
  }, [authLoading, user, router]);

  // Veri Çekme Fonksiyonu
  async function fetchSleepData(endpoint: string) {
    setLoading(true);
    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    try {
      // Token varsa header'a ekle
      const headers: HeadersInit = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const res = await fetch(`${API_URL}${endpoint}`, { headers });
      if (!res.ok) throw new Error('Sunucuya ulaşılamadı');
      const json = await res.json();

      if (json.status === 'success') {
        setData(json.data);
        setNav(json.navigation || { prev_id: null, next_id: null });
        setError(null);
      } else if (json.status === 'empty') {
        // Veri yoksa BOŞ DATA göster
        setData({
          stats: { total_sleep: 0, deep: 0, rem: 0, awake: 0, in_bed: 0 },
          formatted: {
            total: "0s 0dk", deep: "0s 0dk", rem: "0s 0dk", awake: "0s 0dk",
            date: new Date().toLocaleDateString('tr-TR')
          }
        });
        setNav({ prev_id: null, next_id: null });
        setError(null); // Hata sayma, normal durum
      } else {
        setError(json.message || 'Veri bulunamadı.');
      }
    } catch (err: any) {
      setError(err.message || 'Bir hata oluştu.');
    } finally {
      setLoading(false);
    }
  }

  // İlk Açılış: Son Veriyi Getir
  useEffect(() => {
    fetchSleepData('/latest-sleep');
  }, []);

  // --- OLAĞANÜSTÜ DURUMLAR ---
  if (loading && !data) return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
    </div>
  );

  // Sadece Gerçek Hatalar İçin (Sunucu Hatası vb.)
  if (error && !data) return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6 text-center">
      <div className="text-4xl mb-4">⚠️</div>
      <p className="text-gray-400">{error}</p>
      <button onClick={() => fetchSleepData('/latest-sleep')} className="mt-4 px-4 py-2 bg-gray-800 rounded-lg">Tekrar Dene</button>
    </div>
  );

  // Veri yoksa Data null gelebilir, ama yukarıda 'empty' durumunda dummy data set ediyoruz.
  // Yine de güvenlik önlemi:
  if (!data) return null;

  const score = Math.min(100, Math.max(0, Math.round((data.stats.total_sleep / 480) * 100)));
  const isEmptySession = data.stats.total_sleep === 0; // Veri boş mu kontrolü

  return (
    <main className="min-h-screen text-white px-6 py-4 flex flex-col items-center max-w-md mx-auto relative z-10 overflow-y-auto pb-32">
      {/* Yıldızlı Gece Arka Planı */}
      <StarryBackground />

      {/* Loading Overlay (Geçişlerde) */}
      {loading && (
        <div className="absolute inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
          <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}

      {/* Üst Bar ve Navigasyon */}
      <header className="w-full flex justify-between items-center mb-6 sticky top-0 pt-4 pb-2 z-20">
        <div className="flex items-center gap-3">
          <div className="flex flex-col">
            <h1 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent leading-none">
              SleepCoach
            </h1>
            {user?.username && (
              <span className="text-[10px] sm:text-xs text-gray-500 font-medium tracking-wide mt-0.5">
                @{user.username}
              </span>
            )}
          </div>

          {/* Çıkış Butonu */}
          <button
            onClick={() => { logout(); router.push('/auth'); }}
            className="text-gray-500 hover:text-red-400 transition-colors p-1"
            title="Çıkış Yap"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
          </button>
        </div>

        {/* Tarih ve Oklar - Şeffaf Görünüm */}
        <div className="flex items-center gap-3 text-white">
          <button
            disabled={!nav.prev_id}
            onClick={() => nav.prev_id && fetchSleepData(`/sleep/${nav.prev_id}`)}
            className={`text-lg transition-colors ${nav.prev_id ? 'text-white hover:text-purple-400' : 'text-gray-700 cursor-not-allowed'}`}
          >
            ◀
          </button>

          <span className="text-xs font-mono text-gray-300 min-w-[100px] text-center">
            {data.formatted.date}
          </span>

          <button
            disabled={!nav.next_id}
            onClick={() => nav.next_id && fetchSleepData(`/sleep/${nav.next_id}`)}
            className={`text-lg transition-colors ${nav.next_id ? 'text-white hover:text-purple-400' : 'text-gray-700 cursor-not-allowed'}`}
          >
            ▶
          </button>
        </div>
      </header>

      {/* Ana Skor Kartı */}
      <div className="relative w-64 h-64 flex items-center justify-center mb-8 shrink-0 z-10">
        <div className="absolute inset-0 rounded-full border-4 border-gray-900"></div>
        <div
          className="absolute inset-0 rounded-full border-4 border-purple-500 border-t-transparent transition-all duration-1000"
          style={{ transform: `rotate(${score * 3.6}deg)`, opacity: isEmptySession ? 0.3 : 1 }}
        ></div>

        <div className="text-center z-10">
          <span className="block text-7xl font-black text-white tracking-tighter">
            {score}
          </span>
          <span className="text-gray-500 text-[10px] tracking-[0.2em] uppercase mt-2 font-bold">Uyku Skoru</span>
        </div>
      </div>

      {/* İstatistik Grid */}
      <div className={`grid grid-cols-2 gap-3 w-full mb-6 relative z-10 ${isEmptySession ? 'opacity-50 grayscale' : ''}`}>
        <StatCard label="TOPLAM" value={data.formatted.total} color="text-white" border="border-gray-800" />
        <StatCard label="DERİN" value={data.formatted.deep} color="text-blue-200" border="border-blue-900/30" />
        <StatCard label="REM" value={data.formatted.rem} color="text-purple-200" border="border-purple-900/30" />
        <StatCard label="UYANIKLIK" value={data.formatted.awake} color="text-red-200" border="border-red-900/30" />
      </div>

      {/* AI Koç Mesajı */}
      <div className="w-full bg-gradient-to-br from-gray-900 to-black rounded-2xl p-5 border border-gray-800 relative z-10 overflow-hidden">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-lg">🤖</span>
          <h2 className="font-bold text-gray-400 text-xs uppercase tracking-wide">Analiz</h2>
        </div>
        <p className="text-gray-300 text-sm leading-relaxed">
          {isEmptySession
            ? "Henüz veri gelmedi usta. Bu gece güzel bir uyku çek, sabah analiz yapalım! 🌙💤"
            : (score > 80
              ? "Mükemmel performans! Vücudun tam şarj olmuş. Bugün zorlu görevler için ideal."
              : score > 50
                ? "Ortalama bir uyku. Biraz daha erken yatsan süper olurdu. Akşam ışıkları kıs."
                : "Düşük performans. Bugün kafeini abartma ve akşam 22:00 gibi yatağa gitmeye çalış. 🌙")
          }
        </p>
      </div>

      {/* Alt Menü İçin Boşluk */}
      <div className="h-24 w-full shrink-0" />
    </main>
  );
}

// Yardımcı Bileşen
function StatCard({ label, value, color, border }: any) {
  return (
    <div className={`bg-gray-900/30 p-4 rounded-xl border ${border} flex flex-col justify-center`}>
      <div className="text-gray-600 text-[9px] uppercase font-black tracking-widest mb-1">{label}</div>
      <div className={`text-xl font-bold ${color} tracking-tight`}>{value}</div>
    </div>
  );
}
