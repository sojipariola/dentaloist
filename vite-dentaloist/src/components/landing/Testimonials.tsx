import { Card, CardContent } from '@/components/ui/Card';
import { Star } from 'lucide-react';

const testimonials = [
  {
    name: 'Dr. Sarah Chen',
    practice: 'Bright Smile Dental',
    role: 'Practice Owner',
    content: 'Dentaloist has transformed how we manage our practice. Patient scheduling is now effortless, and the digital records system has eliminated paperwork completely.',
    rating: 5
  },
  {
    name: 'Dr. Michael Rodriguez',
    practice: 'Family Dental Care',
    role: 'Lead Dentist',
    content: 'The analytics dashboard gives us incredible insights into practice performance. We have increased our patient capacity by 30% since implementing this system.',
    rating: 5
  },
  {
    name: 'Jennifer Park',
    practice: 'Modern Dentistry Group',
    role: 'Office Manager',
    content: 'The billing and insurance claims features have saved us countless hours. Integration was seamless and the support team is incredibly responsive.',
    rating: 5
  }
];

export const Testimonials = () => {
  return (
    <section className="py-20 bg-white px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-slate-900 mb-4">
            Trusted by Dental Professionals
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Join hundreds of dental practices that have transformed their operations with Dentaloist.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="border-0 shadow-lg">
              <CardContent className="p-8">
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <p className="text-slate-700 mb-6 leading-relaxed italic">
                  "{testimonial.content}"
                </p>
                
                <div>
                  <div className="font-semibold text-slate-900">{testimonial.name}</div>
                  <div className="text-slate-600 text-sm">{testimonial.role}</div>
                  <div className="text-slate-500 text-sm">{testimonial.practice}</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};