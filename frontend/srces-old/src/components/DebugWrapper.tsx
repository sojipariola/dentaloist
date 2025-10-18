// frontend/src/components/DebugWrapper.tsx
'use client';

import React from 'react';

export default function DebugWrapper({ children }: { children: React.ReactNode }) {
  React.useEffect(() => {
    // Add error boundary at runtime
    const originalConsoleError = console.error;
    console.error = function(...args) {
      if (args[0] && typeof args[0] === 'string' && args[0].includes('Objects are not valid as a React child')) {
        console.log('Found the object rendering error!', args);
        debugger; // Pause execution to inspect
      }
      originalConsoleError.apply(console, args);
    };

    return () => {
      console.error = originalConsoleError;
    };
  }, []);

  return <>{children}</>;
}