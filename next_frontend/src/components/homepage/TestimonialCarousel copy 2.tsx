'use client';

import { useState, useEffect, useContext, createContext, PropsWithChildren } from 'react';
import { authApi } from '@/lib/api/auth';
import { User, UserRole } from '@/types/user';

// ✅ 1. Define context shape
interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// ✅ 2. Create context WITH generic type — this is critical
const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  login: async () => { throw new Error('Not implemented'); },
  logout: () => {},
});

// ✅ 3. Provider component
export function AuthProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // ✅ Complete mock user — matches User interface exactly
        const mockUser: User = {
          id: 1,
          email: 'dentist@example.com',
          first_name: 'John',
          last_name: 'Doe',
          phone: null,
          avatar_url: null,
          bio: null,
          date_of_birth: null,
          gender: null,
          address: null,
          emergency_contact: null,
          specialization: null,
          license_number: null,
          experience_years: null,
          role: UserRole.DENTIST,
          clinic_name: null,
          organization_id: 'org_123',
          custom_role_id: null,
          is_active: true,
          is_admin: false,
          last_login: null,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          tenant_id: null,
          stripe_customer_id: null,
          permissions: ['view_patient', 'create_appointment'],
          settings: {
            theme: 'light',
            language: 'en',
            email_notifications: true,
            sms_notifications: false,
            push_notifications: true,
            appointment_reminders: true,
            billing_notifications: true,
            timezone: 'UTC',
            date_format: 'MM/DD/YYYY',
            time_format: '12h',
            week_start: 0,
            show_online_status: true,
            allow_profile_view: true,
            high_contrast_mode: false,
            reduced_motion: false,
          },
        };
        setUser(mockUser);
      } catch (error) {
        console.error('Failed to initialize auth:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // In real app, this would call your API
      const mockResponse = {
        token: 'fake-jwt-token',
        user: {
          id: 1,
          email,
          first_name: 'John',
          last_name: 'Doe',
          role: UserRole.DENTIST,
          permissions: ['view_patient', 'create_appointment'],
          organization_id: 'org_123',
          settings: { theme: 'light', language: 'en' },
          is_active: true,
          is_admin: false,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        } as User
      };
      
      if (typeof window !== 'undefined') {
        localStorage.setItem('token', mockResponse.token);
      }
      setUser(mockResponse.user);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
    setUser(null);
  };

  // ✅ This JSX is now 100% type-safe
  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// ✅ 4. Custom hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}