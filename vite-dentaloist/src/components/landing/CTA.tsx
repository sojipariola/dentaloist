import { Button } from '@/components/ui/Button';

export const CTA = () => {
  return (
    <section className="py-20 bg-blue-600 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl font-bold text-white mb-6">
          Ready to Transform Your Dental Practice?
        </h2>
        <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
          Join thousands of dental professionals who have streamlined their practice management with Dentaloist.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" variant="secondary" className="text-lg px-8 py-3 h-auto">
            Start Free Trial
          </Button>
          <Button 
            size="lg" 
            variant="outline" 
            className="text-lg px-8 py-3 h-auto border-white text-white hover:bg-white hover:text-blue-600"
          >
            Schedule Demo
          </Button>
        </div>
        <p className="text-blue-200 mt-4 text-sm">
          No credit card required • 14-day free trial • Cancel anytime
        </p>
      </div>
    </section>
  );
};