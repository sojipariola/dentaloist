// src/components/homepage/TestimonialCarousel.tsx
'use client'; // ✅ MUST be first line

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const testimonials = [
  {
    name: 'Dr. Sarah Johnson',
    role: 'Lead Dentist, SmileCare Dental',
    content: "DentalSys has transformed our practice. We've reduced administrative time by 40% and improved patient satisfaction significantly.",
    avatar: '/placeholder-avatar.jpg'
  },
  {
    name: 'Michael Chen',
    role: 'Practice Manager, BrightSmile Clinic',
    content: "The appointment scheduling and billing features are outstanding. Our staff adapted quickly and our patients love the new system.",
    avatar: '/placeholder-avatar.jpg'
  },
  {
    name: 'Dr. Emily Rodriguez',
    role: 'Orthodontist, PerfectSmile Specialists',
    content: "As a specialist, I need detailed treatment planning tools. DentalSys provides exactly what I need with an intuitive interface.",
    avatar: '/placeholder-avatar.jpg'
  }
];

export function TestimonialCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextTestimonial = () => {
    setCurrentIndex((prev) => (prev + 1) % testimonials.length);
  };

  const prevTestimonial = () => {
    setCurrentIndex((prev) => (prev - 1 + testimonials.length) % testimonials.length);
  };

  return (
    <div className="relative max-w-4xl mx-auto">
      <Card>
        <CardContent className="p-6">
          <blockquote className="text-lg italic text-muted-foreground mb-4">
            "{testimonials[currentIndex].content}"
          </blockquote>
          <div className="flex items-center">
            <div className="w-12 h-12 bg-muted rounded-full flex items-center justify-center mr-4">
              👤
            </div>
            <div>
              <CardTitle className="text-lg">{testimonials[currentIndex].name}</CardTitle>
              <p className="text-sm text-muted-foreground">{testimonials[currentIndex].role}</p>
            </div>
          </div>
        </CardContent>
      </Card>
      <div className="flex justify-center mt-4 space-x-2">
        <button 
          onClick={prevTestimonial}
          className="p-2 rounded-full hover:bg-muted transition-colors"
        >
          ←
        </button>
        {testimonials.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentIndex(index)}
            className={`w-3 h-3 rounded-full transition-colors ${
              index === currentIndex ? 'bg-primary' : 'bg-muted'
            }`}
          />
        ))}
        <button 
          onClick={nextTestimonial}
          className="p-2 rounded-full hover:bg-muted transition-colors"
        >
          →
        </button>
      </div>
    </div>
  );
}