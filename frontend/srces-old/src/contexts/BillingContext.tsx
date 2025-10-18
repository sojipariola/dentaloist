// frontend/src/contexts/BillingContext.tsx
'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface BillingContextType {
  billingInfo: Record<string, any> | null;
  setBillingInfo: (info: Record<string, any>) => void;
}

const BillingContext = createContext<BillingContextType | undefined>(undefined);

export const BillingProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [billingInfo, setBillingInfo] = useState<Record<string, any> | null>(null);

  return (
    <BillingContext.Provider value={{ billingInfo, setBillingInfo }}>
      {children}
    </BillingContext.Provider>
  );
};

export const useBilling = (): BillingContextType => {
  const context = useContext(BillingContext);
  if (!context) {
    throw new Error('useBilling must be used within a BillingProvider');
  }
  return context;
};

// Add more billing-related logic as needed