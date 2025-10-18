// frontend/src/app/layout.tsx

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from './lib/auth'  

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Dentaloist - Dental Practice Management',
  description: 'Modern dental practice management software',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}