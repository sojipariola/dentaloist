// frontend/src/app/layout.tsx

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/context/AuthContext';
import SimpleErrorBoundary from '@/./components/SimpleErrorBoundary';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Dental SaaS Platform',
  description: 'Comprehensive dental practice management software',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <SimpleErrorBoundary>
          <AuthProvider>
            {children}
          </AuthProvider>
        </SimpleErrorBoundary>
      </body>
    </html>
  );
}