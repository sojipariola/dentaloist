import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const features = [
  {
    title: 'Appointment Scheduling',
    description: 'Easily manage patient appointments with our intuitive calendar system.',
    icon: '📅'
  },
  {
    title: 'Patient Records',
    description: 'Securely store and access comprehensive patient medical histories.',
    icon: '📋'
  },
  {
    title: 'Billing & Invoicing',
    description: 'Streamline your financial operations with automated billing and payment tracking.',
    icon: '💳'
  },
  {
    title: 'Treatment Planning',
    description: 'Create and track detailed treatment plans with progress monitoring.',
    icon: '🦷'
  },
  {
    title: 'Inventory Management',
    description: 'Keep track of supplies and equipment with automated inventory alerts.',
    icon: '📦'
  },
  {
    title: 'Analytics & Reporting',
    description: 'Gain insights into your practice performance with customizable reports.',
    icon: '📊'
  }
];

export function FeatureGrid() {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {features.map((feature, index) => (
        <Card key={index}>
          <CardHeader>
            <div className="text-4xl mb-2">{feature.icon}</div>
            <CardTitle>{feature.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{feature.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
