'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/lib/hooks/useAuth';
import { hasPermission } from '@/lib/utils/permissions';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', permission: null },
  { name: 'Patients', href: '/dashboard', permission: 'view_patient' },
  { name: 'Appointments', href: '/dashboard', permission: 'view_appointment' },
  { name: 'Billing', href: '/dashboard', permission: 'view_billing' },
  { name: 'Lab Orders', href: '/dashboard', permission: 'view_treatment' },
  { name: 'Inventory', href: '/dashboard', permission: 'manage_inventory' },
  { name: 'Reports', href: '/dashboard', permission: 'view_analytics' },
  { name: 'Settings', href: '/dashboard', permission: 'edit_organization' },
];

export function Sidebar() {
  const { user } = useAuth();
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  if (!user) return null;

  return (
    <aside className="hidden w-64 flex-col border-r bg-muted/40 md:flex">
      <div className="flex h-14 items-center border-b px-4">
        <h2 className="font-semibold">Navigation</h2>
      </div>
      <nav className="flex-1 overflow-y-auto p-4">
        <ul className="space-y-2">
          {navigation.map((item) => {
            if (item.permission && !hasPermission(user, item.permission)) {
              return null;
            }
            return (
              <li key={item.name}>
                <Link href={item.href} passHref>
                  <Button
                    variant={pathname === item.href ? "secondary" : "ghost"}
                    className="w-full justify-start"
                  >
                    {item.name}
                  </Button>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}
