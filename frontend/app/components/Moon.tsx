'use client';

import { motion } from 'framer-motion';

// ============================================
// 🌙 AY KOMPONENTİ (Hilal → Dolunay Animasyonu)
// ============================================

interface MoonProps {
    size?: number;
    animate?: boolean;
}

export default function Moon({ size = 120, animate = true }: MoonProps) {
    return (
        <div className="relative" style={{ width: size, height: size }}>
            {/* Ana Ay */}
            <motion.div
                className="absolute inset-0 rounded-full"
                style={{
                    background: 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%)',
                    boxShadow: '0 0 60px rgba(251, 191, 36, 0.5), 0 0 120px rgba(251, 191, 36, 0.3)',
                }}
                animate={animate ? {
                    boxShadow: [
                        '0 0 60px rgba(251, 191, 36, 0.4), 0 0 120px rgba(251, 191, 36, 0.2)',
                        '0 0 80px rgba(251, 191, 36, 0.6), 0 0 160px rgba(251, 191, 36, 0.4)',
                        '0 0 60px rgba(251, 191, 36, 0.4), 0 0 120px rgba(251, 191, 36, 0.2)',
                    ],
                } : {}}
                transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: 'easeInOut',
                }}
            >
                {/* Ay Kraterleri (Detay) */}
                <div
                    className="absolute rounded-full opacity-20"
                    style={{
                        width: size * 0.2,
                        height: size * 0.2,
                        top: '20%',
                        left: '25%',
                        background: 'rgba(0, 0, 0, 0.3)',
                    }}
                />
                <div
                    className="absolute rounded-full opacity-15"
                    style={{
                        width: size * 0.15,
                        height: size * 0.15,
                        top: '50%',
                        left: '60%',
                        background: 'rgba(0, 0, 0, 0.3)',
                    }}
                />
                <div
                    className="absolute rounded-full opacity-10"
                    style={{
                        width: size * 0.1,
                        height: size * 0.1,
                        top: '70%',
                        left: '30%',
                        background: 'rgba(0, 0, 0, 0.3)',
                    }}
                />
            </motion.div>

            {/* Hilal Efekti (Animasyonlu gölge - Hilalden Dolunaya) */}
            {animate && (
                <motion.div
                    className="absolute inset-0 rounded-full"
                    style={{
                        background: 'linear-gradient(90deg, #0a0a1a 0%, transparent 100%)',
                    }}
                    initial={{ opacity: 0.9, x: -size * 0.1 }}
                    animate={{
                        opacity: [0.9, 0, 0],
                        x: [-size * 0.1, size * 0.3, size * 0.5],
                    }}
                    transition={{
                        duration: 3,
                        ease: 'easeOut',
                    }}
                />
            )}
        </div>
    );
}
