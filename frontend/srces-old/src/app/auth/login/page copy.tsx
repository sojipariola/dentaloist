import { Metadata } from 'next';
import { LoginForm } from '@/features/auth/components/LoginForm';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Login - Dental SaaS',
  description: 'Sign in to your Dental SaaS account',
};

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <LoginForm />
        
        <div className="text-center">
          <Link 
            href="/auth/register" 
            className="font-medium text-blue-600 hover:text-blue-500"
          >
            Don't have an account? Sign up
          </Link>
        </div>
      </div>
    </div>
  );
}