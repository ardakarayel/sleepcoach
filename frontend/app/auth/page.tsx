'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import StarryBackground from '../components/StarryBackground';
import Moon from '../components/Moon';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/navigation';

// ============================================
// 🔐 AUTH PAGE - Giriş / Kayıt Sayfası
// ============================================

type AuthMode = 'welcome' | 'login' | 'register';

// Sayfa geçiş animasyonları
const pageVariants = {
    initial: { opacity: 0, x: 100 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -100 },
};

const pageTransition = {
    type: 'spring' as const,
    stiffness: 300,
    damping: 30,
};

export default function AuthPage() {
    const [mode, setMode] = useState<AuthMode>('welcome');
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { login, register } = useAuth();
    const router = useRouter();

    // Form gönderimi
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsSubmitting(true);

        try {
            if (mode === 'login') {
                const result = await login(email, password);
                if (result.success) {
                    router.push('/');
                } else {
                    setError(result.error || 'Giriş başarısız');
                }
            } else if (mode === 'register') {
                if (password.length < 6) {
                    setError('Şifre en az 6 karakter olmalı');
                    setIsSubmitting(false);
                    return;
                }
                const result = await register(email, username, password);
                if (result.success) {
                    router.push('/');
                } else {
                    setError(result.error || 'Kayıt başarısız');
                }
            }
        } catch (err) {
            setError('Bir hata oluştu');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
            {/* Yıldızlı Arka Plan */}
            <StarryBackground />

            {/* Ana İçerik */}
            <div className="relative z-10 w-full max-w-md mx-4">
                <AnimatePresence mode="wait">
                    {/* ===================== HOŞ GELDİN EKRANI ===================== */}
                    {mode === 'welcome' && (
                        <motion.div
                            key="welcome"
                            variants={pageVariants}
                            initial="initial"
                            animate="animate"
                            exit="exit"
                            transition={pageTransition}
                            className="text-center"
                        >
                            {/* Ay */}
                            <motion.div
                                className="flex justify-center mb-8"
                                initial={{ y: -50, opacity: 0 }}
                                animate={{ y: 0, opacity: 1 }}
                                transition={{ delay: 0.2, duration: 0.8 }}
                            >
                                <Moon size={140} animate={true} />
                            </motion.div>

                            {/* Logo & Slogan */}
                            <motion.h1
                                className="text-4xl font-bold mb-3"
                                initial={{ y: 20, opacity: 0 }}
                                animate={{ y: 0, opacity: 1 }}
                                transition={{ delay: 0.5 }}
                                style={{
                                    background: 'linear-gradient(135deg, #ffffff 0%, #a78bfa 100%)',
                                    WebkitBackgroundClip: 'text',
                                    WebkitTextFillColor: 'transparent',
                                }}
                            >
                                SleepCoach
                            </motion.h1>

                            <motion.p
                                className="text-gray-400 text-lg mb-10"
                                initial={{ y: 20, opacity: 0 }}
                                animate={{ y: 0, opacity: 1 }}
                                transition={{ delay: 0.7 }}
                            >
                                Daha iyi uyu, daha iyi yaşa 🌙
                            </motion.p>

                            {/* Butonlar */}
                            <motion.div
                                className="space-y-4"
                                initial={{ y: 30, opacity: 0 }}
                                animate={{ y: 0, opacity: 1 }}
                                transition={{ delay: 0.9 }}
                            >
                                <button
                                    onClick={() => setMode('login')}
                                    className="btn-primary w-full text-lg"
                                >
                                    Giriş Yap
                                </button>
                                <button
                                    onClick={() => setMode('register')}
                                    className="btn-secondary w-full text-lg"
                                >
                                    Kayıt Ol
                                </button>
                            </motion.div>
                        </motion.div>
                    )}

                    {/* ===================== GİRİŞ FORMU ===================== */}
                    {mode === 'login' && (
                        <motion.div
                            key="login"
                            variants={pageVariants}
                            initial="initial"
                            animate="animate"
                            exit="exit"
                            transition={pageTransition}
                        >
                            <div className="glass-card p-8">
                                {/* Başlık */}
                                <div className="text-center mb-8">
                                    <Moon size={60} animate={false} />
                                    <h2 className="text-2xl font-bold mt-4">Hoş Geldin! 👋</h2>
                                    <p className="text-gray-400 mt-2">Hesabına giriş yap</p>
                                </div>

                                {/* Form */}
                                <form onSubmit={handleSubmit} className="space-y-5">
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Email</label>
                                        <input
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            className="glass-input w-full px-4 py-3"
                                            placeholder="ornek@email.com"
                                            required
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Şifre</label>
                                        <input
                                            type="password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            className="glass-input w-full px-4 py-3"
                                            placeholder="••••••••"
                                            required
                                        />
                                    </div>

                                    {error && (
                                        <motion.p
                                            className="text-red-400 text-sm text-center"
                                            initial={{ opacity: 0, y: -10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                        >
                                            {error}
                                        </motion.p>
                                    )}

                                    <button
                                        type="submit"
                                        disabled={isSubmitting}
                                        className="btn-primary w-full text-lg disabled:opacity-50"
                                    >
                                        {isSubmitting ? 'Giriş yapılıyor...' : 'Giriş Yap'}
                                    </button>
                                </form>

                                {/* Alt Link */}
                                <p className="text-center text-gray-400 mt-6">
                                    Hesabın yok mu?{' '}
                                    <button
                                        onClick={() => { setMode('register'); setError(''); }}
                                        className="text-purple-400 hover:text-purple-300 font-medium"
                                    >
                                        Kayıt Ol
                                    </button>
                                </p>

                                {/* Geri Butonu */}
                                <button
                                    onClick={() => { setMode('welcome'); setError(''); }}
                                    className="w-full text-gray-500 hover:text-gray-300 mt-4 text-sm"
                                >
                                    ← Geri
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {/* ===================== KAYIT FORMU ===================== */}
                    {mode === 'register' && (
                        <motion.div
                            key="register"
                            variants={pageVariants}
                            initial="initial"
                            animate="animate"
                            exit="exit"
                            transition={pageTransition}
                        >
                            <div className="glass-card p-8">
                                {/* Başlık */}
                                <div className="text-center mb-8">
                                    <Moon size={60} animate={false} />
                                    <h2 className="text-2xl font-bold mt-4">Aramıza Katıl! ✨</h2>
                                    <p className="text-gray-400 mt-2">Yeni hesap oluştur</p>
                                </div>

                                {/* Form */}
                                <form onSubmit={handleSubmit} className="space-y-5">
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Email</label>
                                        <input
                                            type="email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            className="glass-input w-full px-4 py-3"
                                            placeholder="ornek@email.com"
                                            required
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Kullanıcı Adı</label>
                                        <input
                                            type="text"
                                            value={username}
                                            onChange={(e) => setUsername(e.target.value)}
                                            className="glass-input w-full px-4 py-3"
                                            placeholder="arda123"
                                            required
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Şifre</label>
                                        <input
                                            type="password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            className="glass-input w-full px-4 py-3"
                                            placeholder="En az 6 karakter"
                                            required
                                            minLength={6}
                                        />
                                    </div>

                                    {error && (
                                        <motion.p
                                            className="text-red-400 text-sm text-center"
                                            initial={{ opacity: 0, y: -10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                        >
                                            {error}
                                        </motion.p>
                                    )}

                                    <button
                                        type="submit"
                                        disabled={isSubmitting}
                                        className="btn-primary w-full text-lg disabled:opacity-50"
                                    >
                                        {isSubmitting ? 'Kayıt yapılıyor...' : 'Kayıt Ol'}
                                    </button>
                                </form>

                                {/* Alt Link */}
                                <p className="text-center text-gray-400 mt-6">
                                    Zaten hesabın var mı?{' '}
                                    <button
                                        onClick={() => { setMode('login'); setError(''); }}
                                        className="text-purple-400 hover:text-purple-300 font-medium"
                                    >
                                        Giriş Yap
                                    </button>
                                </p>

                                {/* Geri Butonu */}
                                <button
                                    onClick={() => { setMode('welcome'); setError(''); }}
                                    className="w-full text-gray-500 hover:text-gray-300 mt-4 text-sm"
                                >
                                    ← Geri
                                </button>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
