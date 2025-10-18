'use client';

import { Button } from '@/components/ui/button';
import { useAuth } from '@/lib/hooks/useAuth';
import Link from 'next/link';
import { ThemeToggle } from './ThemeToggle';

export function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="hidden font-bold sm:inline-block">
              DentalSys
            </span>
          </Link>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center space-x-2">
            <ThemeToggle />
            {user && (
              <div className="flex items-center space-x-4">
                <span className="text-sm">
                  Welcome, {user.first_name}
                </span>
                <Button variant="ghost" size="sm" onClick={logout}>
                  Logout
                </Button>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
