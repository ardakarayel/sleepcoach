'use client';

import { useState, useEffect } from 'react';

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

  // Veri Çekme Fonksiyonu
  async function fetchSleepData(endpoint: string) {
    setLoading(true);
    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    try {
      const res = await fetch(`${API_URL}${endpoint}`);
      if (!res.ok) throw new Error('Sunucuya ulaşılamadı');
      const json = await res.json();

      if (json.status === 'success') {
        setData(json.data);
        setNav(json.navigation || { prev_id: null, next_id: null });
        setError(null);
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

  if (error && !data) return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6 text-center">
      <div className="text-4xl mb-4">⚠️</div>
      <p className="text-gray-400">{error}</p>
      <button onClick={() => fetchSleepData('/latest-sleep')} className="mt-4 px-4 py-2 bg-gray-800 rounded-lg">Tekrar Dene</button>
    </div>
  );

  if (!data) return null;

  const score = Math.min(100, Math.max(0, Math.round((data.stats.total_sleep / 480) * 100)));

  return (
    <main className="min-h-screen bg-black text-white p-6 flex flex-col items-center max-w-md mx-auto relative">

      {/* Loading Overlay (Geçişlerde) */}
      {loading && (
        <div className="absolute inset-0 bg-black/50 z-50 flex items-center justify-center backdrop-blur-sm">
          <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}

      {/* Üst Bar ve Navigasyon */}
      <header className="w-full flex justify-between items-center mb-6">
        <h1 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
          SleepCoach
        </h1>

        {/* Tarih ve Oklar */}
        <div className="flex items-center gap-3 bg-gray-900/80 px-3 py-1.5 rounded-full border border-gray-800">
          <button
            disabled={!nav.prev_id}
            onClick={() => nav.prev_id && fetchSleepData(`/sleep/${nav.prev_id}`)}
            className={`text-lg ${nav.prev_id ? 'text-white hover:text-purple-400' : 'text-gray-700 cursor-not-allowed'}`}
          >
            ◀
          </button>

          <span className="text-xs font-mono text-gray-300 min-w-[100px] text-center">
            {data.formatted.date}
          </span>

          <button
            disabled={!nav.next_id}
            onClick={() => nav.next_id && fetchSleepData(`/sleep/${nav.next_id}`)}
            className={`text-lg ${nav.next_id ? 'text-white hover:text-purple-400' : 'text-gray-700 cursor-not-allowed'}`}
          >
            ▶
          </button>
        </div>
      </header>

      {/* Ana Skor Kartı */}
      <div className="relative w-64 h-64 flex items-center justify-center mb-8 shrink-0">
        <div className="absolute inset-0 rounded-full border-4 border-gray-900"></div>
        <div
          className="absolute inset-0 rounded-full border-4 border-purple-500 border-t-transparent transition-all duration-1000"
          style={{ transform: `rotate(${score * 3.6}deg)` }}
        ></div>

        <div className="text-center z-10">
          <span className="block text-7xl font-black text-white tracking-tighter">
            {score}
          </span>
          <span className="text-gray-500 text-[10px] tracking-[0.2em] uppercase mt-2 font-bold">Uyku Skoru</span>
        </div>
      </div>

      {/* İstatistik Grid */}
      <div className="grid grid-cols-2 gap-3 w-full mb-6">
        <StatCard label="TOPLAM" value={data.formatted.total} color="text-white" border="border-gray-800" />
        <StatCard label="DERİN" value={data.formatted.deep} color="text-blue-200" border="border-blue-900/30" />
        <StatCard label="REM" value={data.formatted.rem} color="text-purple-200" border="border-purple-900/30" />
        <StatCard label="UYANIKLIK" value={data.formatted.awake} color="text-red-200" border="border-red-900/30" />
      </div>

      {/* AI Koç Mesajı */}
      <div className="w-full bg-gradient-to-br from-gray-900 to-black rounded-2xl p-5 border border-gray-800 relative overflow-hidden">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-lg">🤖</span>
          <h2 className="font-bold text-gray-400 text-xs uppercase tracking-wide">Analiz</h2>
        </div>
        <p className="text-gray-300 text-sm leading-relaxed">
          {score > 80
            ? "Mükemmel performans! Vücudun tam şarj olmuş. Bugün zorlu görevler için ideal."
            : score > 50
              ? "Ortalama bir uyku. Biraz daha erken yatsan süper olurdu. Akşam ışıkları kıs."
              : "Düşük performans. Bugün kafeini abartma ve akşam 22:00 gibi yatağa gitmeye çalış. 🌙"
          }
        </p>
      </div>

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
