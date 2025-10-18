// frontend/src/contexts/ProfileContext.tsx
'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ProfileContextType {
  profile: Record<string, any> | null;
  setProfile: (profile: Record<string, any>) => void;
}

const ProfileContext = createContext<ProfileContextType | undefined>(undefined);

export const ProfileProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [profile, setProfile] = useState<Record<string, any> | null>(null);

  return (
    <ProfileContext.Provider value={{ profile, setProfile }}>
      {children}
    </ProfileContext.Provider>
  );
};

export const useProfile = (): ProfileContextType => {
  const context = useContext(ProfileContext);
  if (!context) {
    throw new Error('useProfile must be used within a ProfileProvider');
  }
  return context;
};

// Add more profile-related logic as needed