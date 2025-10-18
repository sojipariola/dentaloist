import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/Card';
import { Check } from 'lucide-react';

const plans = [
  {
    name: 'Starter',
    description: 'Perfect for solo practitioners',
    price: '$99',
    period: '/month',
    features: [
      'Up to 500 patients',
      'Basic appointment scheduling',
      'Patient records management',
      'Email support',
      'Basic reporting'
    ]
  },
  {
    name: 'Professional',
    description: 'Ideal for growing practices',
    price: '$199',
    period: '/month',
    popular: true,
    features: [
      'Up to 2000 patients',
      'Advanced scheduling',
      'Treatment planning',
      'Billing & invoicing',
      'Priority support',
      'Custom forms'
    ]
  },
  {
    name: 'Enterprise',
    description: 'For multi-location clinics',
    price: 'Custom',
    period: '',
    features: [
      'Unlimited patients',
      'Multi-location support',
      'Advanced analytics',
      'API access',
      'Dedicated manager',
      'Custom integrations',
      'Training & onboarding'
    ]
  }
];

export const Pricing = () => {
  return (
    <section className="py-20 bg-slate-50 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-slate-900 mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Start free for 14 days. No credit card required. Cancel anytime.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, index) => (
            <Card 
              key={index} 
              className={`border-2 relative ${
                plan.popular 
                  ? 'border-blue-500 shadow-xl scale-105' 
                  : 'border-slate-200 shadow-lg'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}
              
              <CardHeader className="text-center pb-4">
                <h3 className="text-2xl font-bold text-slate-900">{plan.name}</h3>
                <p className="text-slate-600">{plan.description}</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-slate-900">{plan.price}</span>
                  <span className="text-slate-600">{plan.period}</span>
                </div>
              </CardHeader>
              
              <CardContent>
                <ul className="space-y-3">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center gap-3">
                      <Check className="h-5 w-5 text-green-500 flex-shrink-0" />
                      <span className="text-slate-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              
              <CardFooter>
                <Button 
                  className="w-full" 
                  variant={plan.popular ? 'primary' : 'outline'}
                  size="lg"
                >
                  Get Started
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};