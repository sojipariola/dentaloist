'use client';

import { motion } from 'framer-motion';
import Image from 'next/image';
import Link from 'next/link';

export function Hero() {
  return (
    <section className="relative py-20 md:py-32 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-secondary/10"></div>
      <div className="container mx-auto px-4 relative z-10">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Modern Dental Practice Management
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              Streamline appointments, patient records, billing, and more with our all-in-one platform designed for dental professionals.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="/login" className="bg-primary text-primary-foreground px-8 py-4 rounded-full font-bold text-lg hover:bg-primary/90 transition-colors text-center">
                Get Started
              </Link>
              <Link href="#features" className="border border-primary text-primary px-8 py-4 rounded-full font-bold text-lg hover:bg-primary/10 transition-colors text-center">
                Learn More
              </Link>
            </div>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            <div className="relative w-full h-80 md:h-[500px] rounded-2xl overflow-hidden shadow-2xl">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20"></div>
              <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                <path d="M0,0 L100,0 L100,100 Z" fill="url(#gradient)" />
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.1" />
                    <stop offset="100%" stopColor="hsl(var(--secondary))" stopOpacity="0.1" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-4 bg-background rounded-xl p-6 flex flex-col justify-center items-center">
                <div className="text-6xl mb-4">🦷</div>
                <h3 className="text-2xl font-bold text-center">DentalSys Dashboard</h3>
                <p className="text-center text-muted-foreground mt-2">All your practice management tools in one place</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
