import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';        // ✅ Updated path
import '@/styles/theme.css';          // ✅ If you use it
import { ThemeProvider } from '@/components/layout/ThemeProvider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'DentalSys - Modern Dental Practice Management',
  description: 'Streamline your dental practice with our all-in-one management platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
