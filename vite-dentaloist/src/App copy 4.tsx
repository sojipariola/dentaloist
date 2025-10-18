// src/App.tsx - FIXED VERSION
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Toaster } from 'sonner'

// Layout components
import Layout from '@/components/layout/Layout'
import ProtectedRoute from '@/components/auth/ProtectedRoute'

// Page components
import Login from '@/pages/auth/Login'
import Register from '@/pages/auth/Register'
import ForgotPassword from '@/pages/auth/ForgotPassword'
import GithubCallback from '@/pages/auth/GithubCallback'
import Dashboard from '@/pages/dashboard/Dashboard'
import Patients from '@/pages/patients/Patients'
import Appointments from '@/pages/appointments/Appointments'
import Settings from '@/pages/settings/Settings'
import ErrorBoundary from '@/components/error/ErrorBoundary'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <Router>
          <div className="App">
            <Toaster position="top-right" />
            
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/auth/github/callback" element={<GithubCallback />} />
              
              {/* Protected Routes */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="patients" element={<Patients />} />
                <Route path="appointments" element={<Appointments />} />
                <Route path="settings" element={<Settings />} />
              </Route>
              
              {/* Catch all route - 404 */}
              <Route path="*" element={<div>404 - Page Not Found</div>} />
            </Routes>
            
            <ReactQueryDevtools initialIsOpen={false} />
          </div>
        </Router>
      </QueryClientProvider>
    </ErrorBoundary>
  )
}

export default App