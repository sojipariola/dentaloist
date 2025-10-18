import { Hero } from '@/components/landing/Hero';
import { Features } from '@/components/landing/Features';
import { Pricing } from '@/components/landing/Pricing';
import { Testimonials } from '@/components/landing/Testimonials';
import { CTA } from '@/components/landing/CTA';

export const Home = () => {
  return (
    <div className="min-h-screen">
      <Hero />
      <Features />
      <Testimonials />
      <Pricing />
      <CTA />
    </div>
  );
};