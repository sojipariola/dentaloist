// src/App.tsx 

import { BrowserRouter } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import AppRouter from '@/app/router/AppRouter'
import { queryClient } from '@/app/queryClient'
import { ErrorBoundary } from '@/components/error/ErrorBoundary'
import { DebugPanel } from '@/components/debug/DebugPanel'
import { DebugOverlay } from '@/components/dev/DebugOverlay'


function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AppRouter />
          
          {/* ✅ Show debug tools only in development */}
          {import.meta.env.DEV && (
            <>
              <DebugPanel />
              <DebugOverlay />
            </>
          )}
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  )
}

export default App
