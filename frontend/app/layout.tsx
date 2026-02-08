import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { AuthProvider } from './contexts/AuthContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'SleepCoach',
    description: 'AI Destekli Uyku Koçunuz',
    manifest: '/manifest.json',
    icons: {
        icon: '/icon.svg',
        apple: '/apple-touch-icon.png', // iOS için PNG şart
    },
    themeColor: '#0a0a1a',
    appleWebApp: {
        capable: true,
        statusBarStyle: 'black-translucent',
        title: 'SleepCoach',
    },
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="tr">
            <body className={inter.className}>
                <AuthProvider>
                    {children}
                </AuthProvider>
            </body>
        </html>
    )
}

