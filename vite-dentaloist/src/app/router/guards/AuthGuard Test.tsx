import { Routes, Route, Navigate } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import { MainLayout } from '@/components/layout'
import { publicRoutes, privateRoutes, adminRoutes } from './routes'
import { Loader2 } from 'lucide-react'

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

// Temporary bypass component
const TemporaryBypass = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>
}

export default function AppRouter() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <Routes>
        {/* Public routes - No guards at all */}
        <Route path="/" element={<Home />} />
        
        {/* Other public routes without any guards */}
        {publicRoutes.map((route) => (
          <Route
            key={route.path}
            path={route.path}
            element={<route.component />}
          />
        ))}

        {/* Protected routes - Using temporary bypass */}
        <Route
          path="/*"
          element={
            <TemporaryBypass>
              <MainLayout />
            </TemporaryBypass>
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
              element={<route.component />}
            />
          ))}

          {/* Default redirect */}
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