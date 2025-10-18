// next_frontend/src/app/page.tsx
import { Hero } from '@/components/homepage/Hero';
import { FeatureGrid } from '@/components/homepage/FeatureGrid';
import { TestimonialCarousel } from '@/components/homepage/TestimonialCarousel';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      <main className="flex-1">
        <Hero />
        
        <section className="py-20 bg-muted">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">Powerful Features for Modern Dental Practices</h2>
            <FeatureGrid />
          </div>
        </section>

        <section className="py-20">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">What Our Clients Say</h2>
            <TestimonialCarousel />
          </div>
        </section>

        <section className="py-20 bg-primary text-primary-foreground">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to Transform Your Practice?</h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              Join thousands of dental professionals using our platform to streamline operations and improve patient care.
            </p>
            <Link href="/login" className="bg-white text-primary px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-colors">
              Get Started Today
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
