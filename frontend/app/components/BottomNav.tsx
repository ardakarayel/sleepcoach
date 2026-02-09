'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function BottomNav() {
    const pathname = usePathname();

    // Auth sayfalarında menüyü gösterme
    if (pathname.startsWith('/auth')) return null;

    const isActive = (path: string) => pathname === path;

    return (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 w-[90%] max-w-sm bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl flex items-center justify-around p-3 shadow-2xl z-50">

            {/* Ana Sayfa */}
            <Link href="/" className={`p-2 rounded-xl transition-all ${isActive('/') ? 'bg-purple-500/20 text-purple-300' : 'text-gray-500 hover:text-gray-300'}`}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                    <polyline points="9 22 9 12 15 12 15 22" />
                </svg>
            </Link>

            {/* Geçmiş (History) */}
            <Link href="/history" className={`p-2 rounded-xl transition-all ${isActive('/history') ? 'bg-purple-500/20 text-purple-300' : 'text-gray-500 hover:text-gray-300'}`}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                    <line x1="16" y1="2" x2="16" y2="6" />
                    <line x1="8" y1="2" x2="8" y2="6" />
                    <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
            </Link>

            {/* 🤖 DOZIE (AI CHAT) - MERKEZ BUTON */}
            <Link href="/chat" className="relative -top-5 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 p-1 rounded-full shadow-[0_0_20px_rgba(168,85,247,0.5)] transition-transform hover:scale-110">
                <div className="bg-[#0a0a1a] p-3 rounded-full flex items-center justify-center border border-white/20">
                    {/* Robot / Sparkles İkonu */}
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#gradient-icon)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <defs>
                            <linearGradient id="gradient-icon" x1="0" y1="0" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="#c084fc" />
                                <stop offset="100%" stopColor="#f472b6" />
                            </linearGradient>
                        </defs>
                        <path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z" />
                        <path d="M4 11v2a8 8 0 0 0 16 0v-2" />
                        <circle cx="12" cy="14" r="4" />
                        <path d="M12 14h.01" />
                    </svg>
                </div>
            </Link>

            {/* Grafikler / İstatistikler */}
            <Link href="/stats" className={`p-2 rounded-xl transition-all ${isActive('/stats') ? 'bg-purple-500/20 text-purple-300' : 'text-gray-500 hover:text-gray-300'}`}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10" />
                    <line x1="12" y1="20" x2="12" y2="4" />
                    <line x1="6" y1="20" x2="6" y2="14" />
                </svg>
            </Link>

            {/* Profil / Ayarlar */}
            <Link href="/profile" className={`p-2 rounded-xl transition-all ${isActive('/profile') ? 'bg-purple-500/20 text-purple-300' : 'text-gray-500 hover:text-gray-300'}`}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                </svg>
            </Link>

        </div>
    );
}
