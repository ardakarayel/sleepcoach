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

interface Meteor {
    id: number;
    x: number;
    y: number;
    duration: number;
    delay: number;
}

export default function StarryBackground() {
    const [stars, setStars] = useState<Star[]>([]);
    const [meteors, setMeteors] = useState<Meteor[]>([]);

    useEffect(() => {
        // Rastgele yıldızlar oluştur
        const generatedStars: Star[] = [];
        for (let i = 0; i < 70; i++) { // Yıldız sayısını biraz artırdık
            generatedStars.push({
                id: i,
                x: Math.random() * 100,
                y: Math.random() * 100,
                size: Math.random() * 2 + 1, // Biraz daha küçük ve zarif yıldızlar
                delay: Math.random() * 3,
                duration: Math.random() * 3 + 2,
            });
        }
        setStars(generatedStars);

        // Kayan yıldızlar (meteorlar) oluştur
        const generatedMeteors: Meteor[] = [];
        for (let i = 0; i < 4; i++) { // Aynı anda en fazla 4 potansiyel meteor
            generatedMeteors.push({
                id: i,
                x: Math.random() * 100, // Ekranın herhangi bir yerinden başlayabilir (ama yukarıdan)
                y: Math.random() * 50, // Sadece üst yarıdan başlasın
                duration: Math.random() * 1 + 0.5, // 0.5s - 1.5s arası hızlı geçiş
                delay: Math.random() * 10, // İlk başlaması için rastgele bekleme
            });
        }
        setMeteors(generatedMeteors);
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

            {/* Kayan Yıldızlar (Meteor Yağmuru) */}
            {meteors.map((meteor) => (
                <motion.div
                    key={meteor.id}
                    className="absolute h-[2px] bg-gradient-to-r from-white via-transparent to-transparent opacity-0 rounded-full"
                    style={{
                        left: `${meteor.x}%`,
                        top: `${meteor.y}%`,
                        width: '100px', // Kuyruk uzunluğu
                        rotate: '45deg', // Düşüş açısı
                    }}
                    animate={{
                        x: [-100, 200], // Sağ alt köşeye doğru kayış
                        y: [-100, 200],
                        opacity: [0, 1, 0], // Başlangıçta görünür, sonunda kaybolur
                    }}
                    transition={{
                        duration: meteor.duration,
                        delay: meteor.delay,
                        repeat: Infinity,
                        repeatDelay: Math.random() * 10 + 5, // Rastgele tekrar bekleme süresi
                        ease: 'linear',
                    }}
                />
            ))}

            {/* Sabit Yıldızlar */}
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

            {/* Ay (Moon) - Sağ Üst Köşe */}
            <motion.div
                className="absolute top-10 right-10 w-24 h-24 rounded-full bg-yellow-100/10 blur-xl opacity-40 z-0"
                animate={{
                    scale: [1, 1.1, 1],
                    opacity: [0.3, 0.5, 0.3],
                }}
                transition={{
                    duration: 4,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
            />
            <div className="absolute top-12 right-12 w-16 h-16 bg-yellow-100 rounded-full shadow-[0_0_50px_rgba(253,224,71,0.5)] opacity-90 z-0">
                {/* Kraterler */}
                <div className="absolute top-3 left-4 w-3 h-3 bg-yellow-200/50 rounded-full opacity-50"></div>
                <div className="absolute bottom-4 right-5 w-2 h-2 bg-yellow-200/50 rounded-full opacity-50"></div>
                <div className="absolute top-8 right-3 w-1.5 h-1.5 bg-yellow-200/50 rounded-full opacity-50"></div>
            </div>

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
