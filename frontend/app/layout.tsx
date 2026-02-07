import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'SleepCoach',
    description: 'AI Destekli Uyku Koçunuz',
    manifest: '/manifest.json',
    icons: {
        icon: '/icon.svg',
        apple: '/icon.svg',
    },
    themeColor: '#000000',
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
        <html lang="en">
            <body className={inter.className}>{children}</body>
        </html>
    )
}
