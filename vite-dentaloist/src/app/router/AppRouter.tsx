// src/app/router/AppRouter.tsx

import { Routes, Route, Navigate } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import { AuthGuard, RoleGuard } from './guards'
import { MainLayout } from '@/components/layout'
import { publicRoutes, privateRoutes, adminRoutes } from './routes'
import { Loader2 } from 'lucide-react'
import { PublicGuard } from './guards/PublicGuard'

// Lazy load pages for better performance
const Home = lazy(() => import('@/pages/landing/Home'))

const LoadingFallback = () => (
  <div className="min-h-screen flex items-center justify-center">
    <div className="text-center">
      <Loader2 className="h-8 w-8 animate-spin text-primary-600 mx-auto mb-4" />
      <p className="text-gray-600">Loading...</p>
    </div>
  </div>
)

export default function AppRouter() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <Routes>
        {/* Public routes - No AuthGuard at all */}
        <Route path="/" element={<Home />} />
        
        {/* Other public routes without AuthGuard */}
        {publicRoutes.map((route) => (
          <Route
            key={route.path}
            path={route.path}
            element={
              <PublicGuard>
                <route.component />
              </PublicGuard>
            }
          />
        ))}

        {/* Protected routes - Only these use AuthGuard */}
        <Route
          path="/*"
          element={
            <AuthGuard requireAuth={true}>
              <MainLayout />
            </AuthGuard>
          }
        >
          {/* Dashboard and app routes */}
          {privateRoutes.map((route) => (
            <Route
              key={route.path}
              path={route.path.replace(/^\//, '')}
              element={<route.component />}
            />
          ))}

          {/* Admin routes */}
          {adminRoutes.map((route) => (
            <Route
              key={route.path}
              path={route.path.replace(/^\//, '')}
              element={
                <RoleGuard isAdminOnly>
                  <route.component />
                </RoleGuard>
              }
            />
          ))}

          {/* Default redirect for authenticated users */}
          <Route path="" element={<Navigate to="dashboard" replace />} />
        </Route>

        {/* 404 page */}
        <Route path="*" element={
          <div className="min-h-screen flex items-center justify-center">
            <div className="text-center">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
              <p className="text-gray-600 mb-8">Page not found</p>
              <a
                href="/"
                className="text-primary-600 hover:text-primary-500 font-medium"
              >
                Return home
              </a>
            </div>
          </div>
        } />
      </Routes>
    </Suspense>
  )
}