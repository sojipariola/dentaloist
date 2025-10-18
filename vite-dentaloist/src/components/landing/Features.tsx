import { Card, CardContent } from '@/components/ui/Card';
import { Calendar, Users, FileText, Shield, BarChart3, Smartphone } from 'lucide-react';

const features = [
  {
    icon: Calendar,
    title: 'Smart Scheduling',
    description: 'Intelligent appointment booking with automated reminders and calendar sync.'
  },
  {
    icon: Users,
    title: 'Patient Management',
    description: 'Complete patient profiles with medical history, treatment plans, and progress tracking.'
  },
  {
    icon: FileText,
    title: 'Digital Records',
    description: 'Secure, cloud-based patient records accessible from anywhere, anytime.'
  },
  {
    icon: Shield,
    title: 'HIPAA Compliant',
    description: 'Enterprise-grade security ensuring full compliance with healthcare regulations.'
  },
  {
    icon: BarChart3,
    title: 'Practice Analytics',
    description: 'Comprehensive insights into practice performance and patient trends.'
  },
  {
    icon: Smartphone,
    title: 'Mobile Ready',
    description: 'Fully responsive design that works seamlessly across all devices.'
  }
];

export const Features = () => {
  return (
    <section className="py-20 bg-white px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-slate-900 mb-4">
            Everything Your Practice Needs
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Streamline your dental practice with our comprehensive suite of tools designed for modern dentistry.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardContent className="p-8">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};