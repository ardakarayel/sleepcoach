'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

// ============================================
// 🌟 YILDIZLI ARKA PLAN KOMPONENTİ
// ============================================

interface Star {
    id: number;
    x: number;
    y: number;
    size: number;
    delay: number;
    duration: number;
}

export default function StarryBackground() {
    const [stars, setStars] = useState<Star[]>([]);

    useEffect(() => {
        // Rastgele yıldızlar oluştur
        const generatedStars: Star[] = [];
        for (let i = 0; i < 50; i++) {
            generatedStars.push({
                id: i,
                x: Math.random() * 100,
                y: Math.random() * 100,
                size: Math.random() * 3 + 1,
                delay: Math.random() * 3,
                duration: Math.random() * 2 + 2,
            });
        }
        setStars(generatedStars);
    }, []);

    return (
        <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
            {/* Gradyan Arka Plan */}
            <div
                className="absolute inset-0"
                style={{
                    background: 'linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 50%, #0f0f2a 100%)',
                }}
            />

            {/* Yıldızlar */}
            {stars.map((star) => (
                <motion.div
                    key={star.id}
                    className="absolute rounded-full bg-white"
                    style={{
                        left: `${star.x}%`,
                        top: `${star.y}%`,
                        width: star.size,
                        height: star.size,
                    }}
                    animate={{
                        opacity: [0.2, 1, 0.2],
                        scale: [1, 1.3, 1],
                    }}
                    transition={{
                        duration: star.duration,
                        delay: star.delay,
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />
            ))}

            {/* Mor Işık Efekti (Üstte) */}
            <div
                className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] opacity-30"
                style={{
                    background: 'radial-gradient(ellipse at center, rgba(139, 92, 246, 0.4) 0%, transparent 70%)',
                }}
            />

            {/* Mor Işık Efekti (Altta) */}
            <div
                className="absolute bottom-0 right-0 w-[600px] h-[300px] opacity-20"
                style={{
                    background: 'radial-gradient(ellipse at center, rgba(139, 92, 246, 0.5) 0%, transparent 70%)',
                }}
            />
        </div>
    );
}
