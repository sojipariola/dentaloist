import './globals.css'
import { ReactNode } from 'react'
import { AuthProvider } from '@/context/AuthContext'
import Navbar from '@/components/sections/Navbar'
import Footer from '@/components/sections/Footer'

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Navbar />
          <main className="min-h-screen">{children}</main>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  )
}
