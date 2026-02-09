'use client';

// ... imports
import { usePathname } from 'next/navigation';

// ... interfaces

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

interface Cloud {
    id: number;
    y: number;
    size: number;
    duration: number;
    delay: number;
}

export default function StarryBackground() {
    const pathname = usePathname();
    const isHomePage = pathname === '/';
    const [stars, setStars] = useState<Star[]>([]);
    const [meteors, setMeteors] = useState<Meteor[]>([]);
    const [clouds, setClouds] = useState<Cloud[]>([]);
    // ... rest of the component logic (useEffect and return)

    useEffect(() => {
        // Rastgele yıldızlar oluştur
        const generatedStars: Star[] = [];
        for (let i = 0; i < 70; i++) {
            generatedStars.push({
                id: i,
                x: Math.random() * 100,
                y: Math.random() * 100,
                size: Math.random() * 2 + 1,
                delay: Math.random() * 3,
                duration: Math.random() * 3 + 2,
            });
        }
        setStars(generatedStars);

        // Kayan yıldızlar oluştur
        const generatedMeteors: Meteor[] = [];
        for (let i = 0; i < 4; i++) {
            generatedMeteors.push({
                id: i,
                x: Math.random() * 100,
                y: Math.random() * 50,
                duration: Math.random() * 1 + 0.5,
                delay: Math.random() * 10,
            });
        }
        setMeteors(generatedMeteors);

        // Bulutlar oluştur
        const generatedClouds: Cloud[] = [];
        for (let i = 0; i < 3; i++) { // 3 adet büyük, yavaş bulut
            generatedClouds.push({
                id: i,
                y: Math.random() * 40, // Sadece üst yarıda
                size: Math.random() * 200 + 300, // 300px - 500px arası devasa boyut
                duration: Math.random() * 40 + 60, // 60s - 100s arası çok yavaş geçiş
                delay: Math.random() * -50, // Bazıları ekranın ortasından başlaması için negatif delay
            });
        }
        setClouds(generatedClouds);

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

            {/* Bulutlar */}
            {clouds.map((cloud) => (
                <motion.div
                    key={cloud.id}
                    className="absolute bg-white/5 blur-3xl rounded-full"
                    style={{
                        top: `${cloud.y}%`,
                        left: `-20%`, // Ekran dışından başla
                        width: `${cloud.size}px`,
                        height: `${cloud.size / 2}px`,
                    }}
                    animate={{
                        x: ['0vw', '120vw'], // Ekranı baştan sona geç
                    }}
                    transition={{
                        duration: cloud.duration,
                        delay: cloud.delay,
                        repeat: Infinity,
                        ease: "linear",
                    }}
                />
            ))}

            {/* Ay (Moon) - Gökyüzünde Yavaş Hareket */}
            {/* Ay (Moon) - Gökyüzünde Yavaş Hareket (Sadece Ana Sayfada) */}
            {isHomePage && (
                <motion.div
                    className="absolute w-24 h-24 z-0"
                    style={{
                        top: '10%',
                        right: '10%',
                    }}
                    animate={{
                        // Daha az hareket: Sadece kendi bölgesinde hafifçe süzülsün
                        y: [0, 5, 0, -5, 0],
                        x: [0, 2, 0, -2, 0],
                    }}
                    transition={{
                        duration: 10, // Daha sakin bir döngü
                        repeat: Infinity,
                        ease: "easeInOut", // Daha doğal geçiş
                    }}
                >
                    <motion.div
                        className="w-full h-full rounded-full bg-yellow-100/10 blur-xl opacity-40 absolute inset-0"
                        animate={{ scale: [1, 1.1, 1], opacity: [0.3, 0.5, 0.3] }}
                        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                    />
                    <div className="w-16 h-16 bg-yellow-100 rounded-full shadow-[0_0_50px_rgba(253,224,71,0.5)] opacity-90 relative top-4 left-4">
                        {/* Kraterler */}
                        <div className="absolute top-3 left-4 w-3 h-3 bg-yellow-200/50 rounded-full opacity-50"></div>
                        <div className="absolute bottom-4 right-5 w-2 h-2 bg-yellow-200/50 rounded-full opacity-50"></div>
                        <div className="absolute top-8 right-3 w-1.5 h-1.5 bg-yellow-200/50 rounded-full opacity-50"></div>
                    </div>
                </motion.div>
            )}

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
