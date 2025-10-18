// contexts/AuthContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { 
  User, 
  UserRole, 
  LoginCredentials, 
  RegisterData, 
  AuthResponse, 
  PermissionCheck, 
  PermissionCheckResult 
} from '@/types/auth';
import { authService } from '@/services/authService';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  googleLogin: () => void;
  facebookLogin: () => void;
  githubLogin: () => void;
  error: string | null;
  clearError: () => void;
  
  // User role methods
  hasRole: (role: UserRole | string) => boolean;
  hasAnyRole: (roles: (UserRole | string)[]) => boolean;
  hasAllRoles: (roles: (UserRole | string)[]) => boolean;
  isSuperAdmin: () => boolean;
  isOrgAdmin: () => boolean;
  isDentist: () => boolean;
  isLabTechnician: () => boolean;
  isAssistant: () => boolean;
  isNurse: () => boolean;
  isBillingStaff: () => boolean;
  isResearcher: () => boolean;
  isFamilyMember: () => boolean;
  isVisitor: () => boolean;
  isPatient: () => boolean;
  
  // Permission methods
  hasPermission: (permission: string) => boolean;
  hasAnyPermission: (permissions: string[]) => boolean;
  hasAllPermissions: (permissions: string[]) => boolean;
  checkPermissions: (check: PermissionCheck) => PermissionCheckResult;
  getUserPermissions: () => string[];
  getUserRoles: () => string[];
  
  // Organization methods
  isSameOrganization: (organizationId?: number) => boolean;
  canAccessOrganization: (organizationId?: number) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async (): Promise<void> => {
    const token = localStorage.getItem('access_token');
    
    if (token) {
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      } catch (err: any) {
        console.error('Failed to fetch user:', err);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
    
    setIsLoading(false);
  };

  const handleAuthResponse = (response: AuthResponse): void => {
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    setUser(response.user);
    setError(null);
  };

  const clearError = (): void => {
    setError(null);
  };

  // Role methods
  const hasRole = (role: UserRole | string): boolean => {
    if (!user || !user.roles) return false;
    return user.roles.includes(role);
  };

  const hasAnyRole = (roles: (UserRole | string)[]): boolean => {
    if (!user || !user.roles) return false;
    return roles.some(role => user.roles.includes(role));
  };

  const hasAllRoles = (roles: (UserRole | string)[]): boolean => {
    if (!user || !user.roles) return false;
    return roles.every(role => user.roles.includes(role));
  };

  // Specific role checkers
  const isSuperAdmin = (): boolean => hasRole(UserRole.SUPER_ADMIN);
  const isOrgAdmin = (): boolean => hasRole(UserRole.ORG_ADMIN);
  const isDentist = (): boolean => hasRole(UserRole.DENTIST);
  const isLabTechnician = (): boolean => hasRole(UserRole.LAB_TECHNICIAN);
  const isAssistant = (): boolean => hasRole(UserRole.ASSISTANT);
  const isNurse = (): boolean => hasRole(UserRole.NURSE);
  const isBillingStaff = (): boolean => hasRole(UserRole.BILLING_STAFF);
  const isResearcher = (): boolean => hasRole(UserRole.RESEARCHER);
  const isFamilyMember = (): boolean => hasRole(UserRole.FAMILY_MEMBER);
  const isVisitor = (): boolean => hasRole(UserRole.VISITOR);
  const isPatient = (): boolean => hasRole(UserRole.PATIENT);

  // Permission methods
  const hasPermission = (permission: string): boolean => {
    if (!user || !user.permissions) return false;
    return user.permissions.includes(permission);
  };

  const hasAnyPermission = (permissions: string[]): boolean => {
    if (!user || !user.permissions) return false;
    return permissions.some(permission => user.permissions.includes(permission));
  };

  const hasAllPermissions = (permissions: string[]): boolean => {
    if (!user || !user.permissions) return false;
    return permissions.every(permission => user.permissions.includes(permission));
  };

  const checkPermissions = (check: PermissionCheck): PermissionCheckResult => {
    const { requiredPermission, requiredPermissions, requireAll = true } = check;
    
    if (!user || !user.permissions) {
      return { 
        hasPermission: false, 
        missingPermissions: requiredPermissions || (requiredPermission ? [requiredPermission] : []) 
      };
    }

    let permissionsToCheck: string[] = [];
    
    if (requiredPermission) {
      permissionsToCheck = [requiredPermission];
    } else if (requiredPermissions) {
      permissionsToCheck = requiredPermissions;
    } else {
      return { hasPermission: true };
    }

    if (requireAll) {
      const missingPermissions = permissionsToCheck.filter(permission => 
        !user.permissions.includes(permission)
      );
      
      return {
        hasPermission: missingPermissions.length === 0,
        missingPermissions: missingPermissions.length > 0 ? missingPermissions : undefined
      };
    } else {
      const hasAny = permissionsToCheck.some(permission => 
        user.permissions.includes(permission)
      );
      
      return {
        hasPermission: hasAny,
        missingPermissions: hasAny ? undefined : permissionsToCheck
      };
    }
  };

  const getUserPermissions = (): string[] => {
    return user?.permissions || [];
  };

  const getUserRoles = (): string[] => {
    return user?.roles || [];
  };

  // Organization methods
  const isSameOrganization = (organizationId?: number): boolean => {
    if (!user || !organizationId) return false;
    if (isSuperAdmin()) return true;
    return user.organization_id === organizationId;
  };

  const canAccessOrganization = (organizationId?: number): boolean => {
    if (!organizationId) return false;
    if (isSuperAdmin()) return true;
    if (isOrgAdmin() && user?.organization_id === organizationId) return true;
    return user?.organization_id === organizationId;
  };

  const login = async (credentials: LoginCredentials): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await authService.login(credentials);
      handleAuthResponse(response);
    } catch (err: any) {
      setError(err.message || 'Login failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData: RegisterData): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await authService.register(userData);
      handleAuthResponse(response);
    } catch (err: any) {
      setError(err.message || 'Registration failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await authService.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  const googleLogin = (): void => {
    authService.googleLogin();
  };

  const facebookLogin = (): void => {
    authService.facebookLogin();
  };

  const githubLogin = (): void => {
    authService.githubLogin();
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    googleLogin,
    facebookLogin,
    githubLogin,
    error,
    clearError,
    
    // Role methods
    hasRole,
    hasAnyRole,
    hasAllRoles,
    isSuperAdmin,
    isOrgAdmin,
    isDentist,
    isLabTechnician,
    isAssistant,
    isNurse,
    isBillingStaff,
    isResearcher,
    isFamilyMember,
    isVisitor,
    isPatient,
    
    // Permission methods
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    checkPermissions,
    getUserPermissions,
    getUserRoles,
    
    // Organization methods
    isSameOrganization,
    canAccessOrganization,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};