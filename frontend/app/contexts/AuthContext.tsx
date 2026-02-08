'use client';

import { useState, useEffect, createContext, useContext, ReactNode } from 'react';

// ============================================
// 🔐 AUTH CONTEXT - Token ve Kullanıcı Yönetimi
// ============================================

interface User {
    id: number;
    email: string;
    username: string;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
    register: (email: string, username: string, password: string) => Promise<{ success: boolean; error?: string }>;
    logout: () => void;
    getGreeting: () => string;
}

const AuthContext = createContext<AuthContextType | null>(null);

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Sayfa yüklendiğinde token kontrolü
    useEffect(() => {
        const savedToken = localStorage.getItem('sleepcoach_token');
        const savedUser = localStorage.getItem('sleepcoach_user');

        if (savedToken && savedUser) {
            setToken(savedToken);
            setUser(JSON.parse(savedUser));
        }
        setIsLoading(false);
    }, []);

    // 🔑 Giriş Yap
    const login = async (email: string, password: string) => {
        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || 'Giriş başarısız' };
            }

            // Token ve kullanıcıyı kaydet
            localStorage.setItem('sleepcoach_token', data.access_token);
            localStorage.setItem('sleepcoach_user', JSON.stringify(data.user));
            setToken(data.access_token);
            setUser(data.user);

            return { success: true };
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: 'Bağlantı hatası' };
        }
    };

    // 📝 Kayıt Ol
    const register = async (email: string, username: string, password: string) => {
        try {
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, username, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || 'Kayıt başarısız' };
            }

            // Token ve kullanıcıyı kaydet (otomatik giriş)
            localStorage.setItem('sleepcoach_token', data.access_token);
            localStorage.setItem('sleepcoach_user', JSON.stringify(data.user));
            setToken(data.access_token);
            setUser(data.user);

            return { success: true };
        } catch (error) {
            console.error('Register error:', error);
            return { success: false, error: 'Bağlantı hatası' };
        }
    };

    // 🚪 Çıkış Yap
    const logout = () => {
        localStorage.removeItem('sleepcoach_token');
        localStorage.removeItem('sleepcoach_user');
        setToken(null);
        setUser(null);
    };

    // ⏰ Saat Bazlı Selamlama
    const getGreeting = () => {
        const hour = new Date().getHours();
        const username = user?.username || 'Misafir';

        if (hour >= 5 && hour < 12) {
            return `Günaydın, ${username}! ☀️`;
        } else if (hour >= 12 && hour < 18) {
            return `İyi günler, ${username}! 🌤️`;
        } else if (hour >= 18 && hour < 22) {
            return `İyi akşamlar, ${username}! 🌅`;
        } else {
            return `İyi geceler, ${username}! 🌙`;
        }
    };

    return (
        <AuthContext.Provider value={{ user, token, isLoading, login, register, logout, getGreeting }}>
            {children}
        </AuthContext.Provider>
    );
}

// Hook
export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
