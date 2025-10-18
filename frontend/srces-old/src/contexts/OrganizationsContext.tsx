// frontend/src/contexts/OrganizationsContext.tsx
'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface OrganizationsContextType {
  organizations: Array<Record<string, any>>;
  setOrganizations: (orgs: Array<Record<string, any>>) => void;
}

const OrganizationsContext = createContext<OrganizationsContextType | undefined>(undefined);

export const OrganizationsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [organizations, setOrganizations] = useState<Array<Record<string, any>>>([]);

  return (
    <OrganizationsContext.Provider value={{ organizations, setOrganizations }}>
      {children}
    </OrganizationsContext.Provider>
  );
};

export const useOrganizations = (): OrganizationsContextType => {
  const context = useContext(OrganizationsContext);
  if (!context) {
    throw new Error('useOrganizations must be used within an OrganizationsProvider');
  }
  return context;
};

// Add more organization-related logic as needed

