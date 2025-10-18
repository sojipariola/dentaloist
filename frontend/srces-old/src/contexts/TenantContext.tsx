// frontend/src/contexts/TenantContext.tsx
'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TenantContextType {
  tenantId: string | null;
  setTenantId: (id: string) => void;
}

const TenantContext = createContext<TenantContextType | undefined>(undefined);

export const TenantProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [tenantId, setTenantId] = useState<string | null>(null);

  return (
    <TenantContext.Provider value={{ tenantId, setTenantId }}>
      {children}
    </TenantContext.Provider>
  );
};

export const useTenant = (): TenantContextType => {
  const context = useContext(TenantContext);
  if (!context) {
    throw new Error('useTenant must be used within a TenantProvider');
  }
  return context;
};

// Add more tenant-related logic as needed