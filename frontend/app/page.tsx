'use client';

import { useState, useEffect } from 'react';

// Tip tanımları (Backend stats'a uygun)
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

export default function Home() {
  const [data, setData] = useState<SleepData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // API URL'sini .env.local'dan al
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    async function fetchData() {
      try {
        const res = await fetch(`${API_URL}/latest-sleep`);

        if (!res.ok) throw new Error('Sunucuya ulaşılamadı');

        const json = await res.json();

        if (json.status === 'success') {
          setData(json.data);
        } else {
          setError(json.message || 'Veri bulunamadı.');
        }
      } catch (err: any) {
        setError(err.message || 'Bir hata oluştu.');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // --- OLAĞANÜSTÜ DURUMLAR ---
  if (loading) return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
    </main>
  );

  if (error) return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6 text-center">
      <div className="text-4xl mb-4">⚠️</div>
      <h2 className="text-xl font-bold mb-2">Ops! Bir sorun var.</h2>
      <p className="text-gray-400">{error}</p>
    </main>
  );

  if (!data) return null;

  // Skor Hesaplama (Basit bir mantık: 8 saat = 100 puan, her eksik saat -10)
  // Bu sadece görsel amaçlıdır, backend'den de çekebilirdik.
  const score = Math.min(100, Math.max(0, Math.round((data.stats.total_sleep / 480) * 100)));

  return (
    <main className="min-h-screen bg-black text-white p-6 flex flex-col items-center max-w-md mx-auto">
      {/* Üst Bar */}
      <header className="w-full flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
          SleepCoach
        </h1>
        <div className="text-xs text-gray-500">{data.formatted.date}</div>
      </header>

      {/* Ana Skor Kartı */}
      <div className="relative w-64 h-64 flex items-center justify-center mb-8">
        <div className="absolute inset-0 rounded-full border-4 border-gray-800"></div>
        <div className="absolute inset-0 rounded-full border-4 border-purple-500 border-t-transparent animate-spin-slow" style={{ animationDuration: '3s' }}></div>

        <div className="text-center">
          <span className="block text-6xl font-black bg-gradient-to-br from-white to-gray-400 bg-clip-text text-transparent">
            {score}
          </span>
          <span className="text-gray-500 text-xs tracking-widest uppercase mt-1">Uyku Skoru</span>
        </div>
      </div>

      {/* AI Koç Mesajı (Şimdilik Statik - İleride Canlı Olacak) */}
      <div className="w-full bg-gray-900/50 backdrop-blur rounded-2xl p-5 mb-6 border border-gray-800/50 relative overflow-hidden group">
        <div className="absolute top-0 left-0 w-1 h-full bg-purple-500"></div>
        <div className="flex items-center gap-3 mb-2">
          <span className="text-xl">🤖</span>
          <h2 className="font-semibold text-purple-200 text-sm uppercase tracking-wide">AI Koçun Notu</h2>
        </div>
        <p className="text-gray-300 text-sm leading-relaxed">
          {score > 80
            ? "Harika bir uyku çekmişsin! Enerjin tavan yapmış durumda. Bugün zor işleri halletmek için mükemmel gün. 🚀"
            : "Biraz uykusuz kalmışsın. Bugün kafein tüketimine dikkat et ve ağır spor yapma. Enerjini koru! 🔋"
          }
        </p>
      </div>

      {/* İstatistik Grid */}
      <div className="grid grid-cols-2 gap-3 w-full">
        {/* Toplam Süre */}
        <div className="bg-gray-900/40 p-4 rounded-xl border border-gray-800/60">
          <div className="text-gray-500 text-[10px] uppercase font-bold tracking-wider mb-1">TOPLAM</div>
          <div className="text-xl font-bold text-white tracking-tight">{data.formatted.total}</div>
        </div>

        {/* Derin Uyku */}
        <div className="bg-gray-900/40 p-4 rounded-xl border border-gray-800/60 transition-colors hover:border-blue-900/50">
          <div className="text-blue-500/70 text-[10px] uppercase font-bold tracking-wider mb-1">DERİN</div>
          <div className="text-xl font-bold text-blue-100 tracking-tight">{data.formatted.deep}</div>
        </div>

        {/* REM */}
        <div className="bg-gray-900/40 p-4 rounded-xl border border-gray-800/60 transition-colors hover:border-purple-900/50">
          <div className="text-purple-500/70 text-[10px] uppercase font-bold tracking-wider mb-1">REM</div>
          <div className="text-xl font-bold text-purple-100 tracking-tight">{data.formatted.rem}</div>
        </div>

        {/* Uyanıklık */}
        <div className="bg-gray-900/40 p-4 rounded-xl border border-gray-800/60 transition-colors hover:border-red-900/50">
          <div className="text-red-500/70 text-[10px] uppercase font-bold tracking-wider mb-1">UYANIKLIK</div>
          <div className="text-xl font-bold text-red-100 tracking-tight">{data.formatted.awake}</div>
        </div>
      </div>

    </main>
  );
}
