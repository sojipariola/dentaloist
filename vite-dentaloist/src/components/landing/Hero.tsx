import { Button } from '@/components/ui/Button';
import { Card, CardContent } from '@/components/ui/Card';
import { ArrowRight, PlayCircle } from 'lucide-react';

export const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-white px-4">
      <div className="absolute inset-0 bg-grid-slate-100 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]" />
      
      <div className="relative max-w-7xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100 text-blue-700 text-sm font-medium mb-8">
          <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
          Streamlining Dental Practices Nationwide
        </div>

        <h1 className="text-5xl md:text-7xl font-bold text-slate-900 mb-6">
          Modern Dental
          <span className="text-blue-600 block">Practice Management</span>
        </h1>

        <p className="text-xl text-slate-600 max-w-3xl mx-auto mb-8 leading-relaxed">
          All-in-one platform to manage appointments, patient records, billing, and inventory. 
          Designed specifically for dental professionals to enhance patient care and practice efficiency.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
          <Button size="lg" className="text-lg px-8 py-3 h-auto">
            Start Free Trial
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
          <Button variant="outline" size="lg" className="text-lg px-8 py-3 h-auto">
            <PlayCircle className="mr-2 h-5 w-5" />
            Watch Demo
          </Button>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-blue-600">500+</div>
              <div className="text-sm text-slate-600">Dental Practices</div>
            </CardContent>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-blue-600">50K+</div>
              <div className="text-sm text-slate-600">Patients Served</div>
            </CardContent>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-blue-600">99.9%</div>
              <div className="text-sm text-slate-600">Uptime</div>
            </CardContent>
          </Card>
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6">
              <div className="text-2xl font-bold text-blue-600">24/7</div>
              <div className="text-sm text-slate-600">Support</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};