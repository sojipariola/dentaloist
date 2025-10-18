// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import DebugWrapper from '@/components/DebugWrapper';
import { AuthProvider } from '@/context/AuthContext';
import Navigation from '@/components/Navigation';
import { UserProvider } from '@/contexts/UserContext';
import { SocketProvider } from '../contexts/SocketContext'
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Dental Management System',
  description: 'Comprehensive dental practice management solution',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <DebugWrapper>
          <AuthProvider>
            <UserProvider>
              <SocketProvider>
                <div className="min-h-screen bg-gray-50">
                  <Navigation />
                  <main className="container mx-auto px-4 py-8">
                    {children}
                  </main>
                </div>
              </SocketProvider>
            </UserProvider>
          </AuthProvider>
        </DebugWrapper>
      </body>
    </html>
  );
}