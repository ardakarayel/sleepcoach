'use client';

import { useState, useRef, useEffect } from 'react';
import StarryBackground from '../components/StarryBackground';

interface Message {
    id: number;
    role: 'user' | 'assistant';
    content: string;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, role: 'assistant', content: "Selam uykucu! Ben Dozie. 😴 Bugün nasıl hissediyorsun? Dün geceki uykun nasıldı?" }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg: Message = { id: Date.now(), role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            // Şimdilik sadece frontend tarafında basit bir cevap simülasyonu yapıyoruz.
            // İleride backend'e bağlanacak.
            setTimeout(() => {
                const aiMsg: Message = {
                    id: Date.now() + 1,
                    role: 'assistant',
                    content: "Hmm... İlgşnç bir durum. Aslında uyku düzenin hakkında biraz daha veri toplarsak sana daha iyi tavsiyeler verebilirim. Şimdilik önerim: Bu akşam kafeini biraz erken kes! ☕❌"
                };
                setMessages(prev => [...prev, aiMsg]);
                setIsLoading(false);
            }, 1500);
        } catch (error) {
            console.error(error);
            setIsLoading(false);
        }
    };

    return (
        <main className="min-h-screen text-white relative flex flex-col pt-4 overflow-hidden">
            <StarryBackground />

            {/* Header */}
            <div className="flex items-center justify-center p-4 border-b border-white/10 z-10 bg-[#0a0a1a]/80 backdrop-blur-md sticky top-0">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-pink-500 p-0.5 mr-3">
                    <div className="w-full h-full bg-black rounded-full flex items-center justify-center">
                        <span className="text-xl">🤖</span>
                    </div>
                </div>
                <div>
                    <h1 className="font-bold text-lg">Dozie</h1>
                    <div className="flex items-center gap-1.5">
                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                        <span className="text-xs text-gray-400">Çevrimiçi (Uyumuyor)</span>
                    </div>
                </div>
            </div>

            {/* Mesaj Alanı */}
            <div className="flex-1 overflow-y-auto p-4 pb-32 space-y-4 z-10 scrollbar-hide">
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] p-4 rounded-2xl ${msg.role === 'user'
                                    ? 'bg-indigo-600 text-white rounded-br-none'
                                    : 'bg-gray-800/80 backdrop-blur-sm text-gray-200 rounded-bl-none border border-white/10'
                                }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-800/80 p-4 rounded-2xl rounded-bl-none border border-white/10 flex items-center gap-1">
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-0"></span>
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
                            <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300"></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Alanı (Fixed Bottom) */}
            <div className="fixed bottom-24 left-0 right-0 p-4 z-20 flex justify-center pointer-events-none">
                <div className="w-full max-w-md bg-gray-900/90 backdrop-blur-xl p-2 rounded-full border border-white/10 shadow-2xl flex items-center gap-2 pointer-events-auto">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Dozie'ye bir şey sor..."
                        className="flex-1 bg-transparent px-4 py-2 outline-none text-white placeholder-gray-500"
                    />
                    <button
                        onClick={handleSend}
                        disabled={isLoading || !input.trim()}
                        className="w-10 h-10 bg-indigo-600 rounded-full flex items-center justify-center hover:bg-indigo-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        </main>
    );
}
