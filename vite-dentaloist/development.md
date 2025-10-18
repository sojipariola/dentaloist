Step 1: Create Project Structure
First, let's create the basic folder structure:

bash
# Create project directory
mkdir vite-dentaloist
cd vite-dentaloist

# Create basic structure
mkdir -p src/{api/{client,endpoints,hooks,services},app/{store,router/{routes,guards}},components/{ui,layout,shared,features,landing},pages/{landing,auth,dashboard,patients,appointments,clinical,billing,inventory,admin,settings},types/{api,forms},utils/{formatters,validators,constants,helpers},hooks,styles}
mkdir -p public/images/{landing,icons}
Step 2: Initialize Package.json
Create package.json:

json
{
  "name": "vite-dentaloist",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.8.4",
    "zustand": "^4.4.7",
    "react-hook-form": "^7.48.2",
    "zod": "^3.22.4",
    "recharts": "^2.8.0",
    "@tanstack/react-table": "^8.10.3",
    "lucide-react": "^0.294.0",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "typescript": "^5.2.2",
    "vite": "^4.5.0"
  }
}
Step 3: Configuration Files
Create vite.config.ts:

typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
Create tsconfig.json:

json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
Create tsconfig.node.json:

json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
Step 4: Tailwind CSS Configuration
Create tailwind.config.js:

javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        dental: {
          blue: '#2563eb',
          teal: '#0d9488',
          green: '#10b981',
          amber: '#f59e0b',
          red: '#ef4444',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
Create postcss.config.js:

javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
Step 5: Basic Styles and Entry Points
Create src/index.css:

css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

@layer base {
  html {
    font-family: 'Inter', system-ui, sans-serif;
  }
  
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200;
  }
  
  .btn-secondary {
    @apply bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 font-medium py-2 px-4 rounded-lg transition-colors duration-200;
  }
  
  .card {
    @apply bg-white rounded-xl shadow-sm border border-gray-200;
  }
  
  .input-field {
    @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent;
  }
}
Create src/main.tsx:

typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
Step 6: Basic App Component
Create src/App.tsx:

typescript
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import AppRouter from '@/app/router/AppRouter'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
Step 7: Landing Page Components
Create src/pages/landing/Home.tsx:

typescript
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  Calendar, 
  Users, 
  DollarSign, 
  Stethoscope, 
  Package, 
  Shield,
  ArrowRight,
  CheckCircle2,
  Play
} from 'lucide-react'

export default function Home() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const features = [
    {
      icon: Calendar,
      title: 'Appointment Management',
      description: 'Streamline scheduling, reminders, and patient communications'
    },
    {
      icon: Users,
      title: 'Patient Management',
      description: 'Comprehensive patient records and medical history tracking'
    },
    {
      icon: DollarSign,
      title: 'Billing & Insurance',
      description: 'Automated invoicing, payment processing, and insurance claims'
    },
    {
      icon: Stethoscope,
      title: 'Clinical Tools',
      description: 'Treatment planning, clinical notes, and prescription management'
    },
    {
      icon: Package,
      title: 'Inventory Management',
      description: 'Track supplies, manage orders, and optimize stock levels'
    },
    {
      icon: Shield,
      title: 'Security & Compliance',
      description: 'HIPAA-compliant security with audit trails and role-based access'
    }
  ]

  const testimonials = [
    {
      name: 'Dr. Sarah Johnson',
      role: 'Dental Practice Owner',
      content: 'Dentaloist transformed our practice. We\'ve reduced administrative work by 60% and improved patient satisfaction significantly.',
      practice: 'Bright Smile Dental'
    },
    {
      name: 'Dr. Michael Chen',
      role: 'Orthodontist',
      content: 'The inventory management alone saved us thousands in optimized supply ordering. The clinical tools are exceptional.',
      practice: 'Perfect Teeth Orthodontics'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Stethoscope className="h-8 w-8 text-primary-600" />
              <span className="text-2xl font-bold text-gray-900">Dentaloist</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">Features</a>
              <a href="#testimonials" className="text-gray-600 hover:text-gray-900 transition-colors">Testimonials</a>
              <a href="#pricing" className="text-gray-600 hover:text-gray-900 transition-colors">Pricing</a>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login" className="text-gray-600 hover:text-gray-900 transition-colors">
                Sign In
              </Link>
              <Link 
                to="/register" 
                className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors font-medium"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className={`text-center space-y-8 transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 leading-tight">
              Modern Dental Practice
              <span className="block text-primary-600">Management</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Streamline your dental practice with all-in-one software for appointments, 
              patient records, billing, and inventory management.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
              <Link 
                to="/register" 
                className="bg-primary-600 text-white px-8 py-4 rounded-xl hover:bg-primary-700 transition-all duration-200 font-semibold text-lg flex items-center space-x-2 shadow-lg hover:shadow-xl"
              >
                <span>Start Free Trial</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <button className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl hover:border-gray-400 transition-all duration-200 font-semibold text-lg flex items-center space-x-2">
                <Play className="h-5 w-5" />
                <span>Watch Demo</span>
              </button>
            </div>
            <div className="pt-8">
              <p className="text-gray-500 text-sm">Trusted by 500+ dental practices worldwide</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Everything Your Practice Needs
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Comprehensive tools designed specifically for dental professionals to save time and grow your practice.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div 
                key={feature.title}
                className="card p-8 hover:shadow-lg transition-all duration-300 group"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-6 group-hover:bg-primary-200 transition-colors">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Loved by Dental Professionals
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              See how Dentaloist is transforming dental practices around the world.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {testimonials.map((testimonial, index) => (
              <div 
                key={testimonial.name}
                className="card p-8 relative"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <div className="absolute -top-4 -left-4 w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                  <CheckCircle2 className="h-5 w-5 text-white" />
                </div>
                <p className="text-gray-700 text-lg italic mb-6">
                  "{testimonial.content}"
                </p>
                <div>
                  <p className="font-semibold text-gray-900">{testimonial.name}</p>
                  <p className="text-gray-600">{testimonial.role}</p>
                  <p className="text-primary-600 font-medium">{testimonial.practice}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Transform Your Practice?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Join thousands of dental professionals who trust Dentaloist to run their practice efficiently.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/register" 
              className="bg-white text-primary-600 px-8 py-4 rounded-xl hover:bg-gray-100 transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl"
            >
              Start Free Trial
            </Link>
            <button className="border-2 border-white text-white px-8 py-4 rounded-xl hover:bg-white hover:text-primary-600 transition-all duration-200 font-semibold text-lg">
              Schedule a Demo
            </button>
          </div>
          <p className="text-primary-200 mt-6 text-sm">
            No credit card required • 14-day free trial • Setup in minutes
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Stethoscope className="h-6 w-6 text-primary-400" />
              <span className="text-xl font-bold">Dentaloist</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2024 Dentaloist. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
Step 8: Basic Router Setup
Create src/app/router/AppRouter.tsx:

typescript
import { Routes, Route } from 'react-router-dom'
import Home from '@/pages/landing/Home'

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<div className="p-8">Login Page - Coming Soon</div>} />
      <Route path="/register" element={<div className="p-8">Register Page - Coming Soon</div>} />
      <Route path="*" element={<div className="p-8 text-center">Page Not Found</div>} />
    </Routes>
  )
}
Step 9: Public Assets
Create public/index.html:

html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Dentaloist - Modern Dental Practice Management Software" />
    <title>Dentaloist - Dental Practice Management</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
Step 10: Install Dependencies
Now run the installation:

bash
# Install all dependencies
npm install

# Start the development server
npm run dev
🎉 Stage 1 Complete!
You now have:

✅ Project Structure - Organized folder structure
✅ Dependencies - All necessary packages installed
✅ Configuration - Vite, TypeScript, Tailwind CSS configured
✅ Landing Page - Professional landing page with features showcase
✅ Development Server - Ready to run on http://localhost:3000

The landing page includes:

Responsive navigation

Hero section with call-to-action

Features grid showcasing all 6 categories from your backend

Testimonials section

Professional footer

Smooth animations and transitions

Next Steps: Run npm run dev to start the development server and verify everything is working. The application should display the landing page at http://localhost:3000.

Ready to proceed to Stage 2 (Foundation)?





# Create placeholder pages
mkdir -p src/pages/{patients,appointments,clinical,billing,inventory,admin,settings}

# Create basic placeholder components
for page in patients/PatientsList patients/PatientDetails patients/PatientForm \
            appointments/AppointmentsList appointments/AppointmentDetails appointments/AppointmentForm \
            clinical/ClinicalRecords billing/Invoices inventory/InventoryItems \
            admin/SystemStats admin/UserManagement admin/RoleManagement admin/SystemSettings \
            settings/Profile settings/Preferences settings/Security settings/Notifications; do
  cat > src/pages/${page}.tsx << 'EOF'
import React from 'react'
import { Card } from '@/components/ui'

export default function Component() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        {(() => {
          const name = location.pathname.split('/').pop() || 'Page'
          return name.charAt(0).toUpperCase() + name.slice(1)
        })()}
      </h1>
      <Card className="p-8">
        <div className="text-center text-gray-500">
          <p className="text-lg">This page is under development</p>
          <p className="text-sm mt-2">Coming soon in Stage 4</p>
        </div>
      </Card>
    </div>
  )
}
EOF
done


# Create placeholder form components
for form in clinical/TreatmentPlanForm clinical/ClinicalNoteForm \
            billing/InvoiceForm billing/PaymentForm \
            inventory/InventoryItemForm; do
  cat > src/pages/${form}.tsx << 'EOF'
import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Button, Card } from '@/components/ui'

export default function Component() {
  const isEdit = location.pathname.includes('/edit')
  
  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="ghost" asChild>
          <Link to="..">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Link>
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">
          {isEdit ? 'Edit' : 'Create New'} {(() => {
            const name = location.pathname.split('/').slice(-2, -1)[0]
            return name.split(/(?=[A-Z])/).join(' ')
          })()}
        </h1>
      </div>

      <Card className="p-8">
        <div className="text-center text-gray-500">
          <p className="text-lg mb-2">Form under development</p>
          <p className="text-sm">This form will be implemented in the next stage</p>
        </div>
      </Card>
    </div>
  )
}
EOF
done






# Create admin form placeholders
for form in admin/UserForm admin/RoleForm admin/SystemStats admin/DatabaseManagement; do
  cat > src/pages/${form}.tsx << 'EOF'
import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Button, Card } from '@/components/ui'

export default function Component() {
  const isEdit = location.pathname.includes('/edit')
  const isNew = location.pathname.includes('/new')
  
  const getPageTitle = () => {
    if (isNew) return 'Create New'
    if (isEdit) return 'Edit'
    return 'System Statistics' // Default for stats page
  }

  const getEntityName = () => {
    const path = location.pathname
    if (path.includes('/users')) return 'User'
    if (path.includes('/roles')) return 'Role'
    if (path.includes('/database')) return 'Database Management'
    return 'System Statistics'
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="ghost" asChild>
          <Link to="..">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Link>
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">
          {getPageTitle()} {getEntityName()}
        </h1>
      </div>

      <Card className="p-8">
        <div className="text-center text-gray-500">
          <p className="text-lg mb-2">
            {isNew || isEdit ? 'Form under development' : 'Page under development'}
          </p>
          <p className="text-sm">
            {isNew || isEdit 
              ? 'This form will be implemented in the next stage'
              : 'This page will be implemented in the next stage'
            }
          </p>
        </div>
      </Card>
    </div>
  )
}
EOF
done

