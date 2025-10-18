'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect } from 'react';

export default function CallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const token = searchParams.get('token');
    if (token) {
      localStorage.setItem('token', token);
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  }, [router, searchParams]);

  return <p className="text-center mt-20">Signing you in...</p>;
}
