import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/app/store'

interface PublicGuardProps {
  children: React.ReactNode
}

export const PublicGuard: React.FC<PublicGuardProps> = ({ children }) => {
  const { isAuthenticated } = useAuthStore()

  // If user is authenticated, redirect them away from public pages (like login)
  // But allow access to landing pages even when authenticated
  const currentPath = window.location.pathname
  
  // Only redirect from auth pages (login, register) if authenticated
  const isAuthPage = ['/login', '/register', '/forgot-password', '/reset-password'].includes(currentPath)
  
  if (isAuthenticated && isAuthPage) {
    return <Navigate to="/dashboard" replace />
  }

  // Allow access to all other public pages (landing pages, features, etc.)
  return <>{children}</>
}