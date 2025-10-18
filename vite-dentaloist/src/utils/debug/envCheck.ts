// Environment validation for development
export const checkEnvironment = () => {
  const issues: string[] = []

  // Check required environment variables
  if (!import.meta.env.VITE_API_URL) {
    issues.push('VITE_API_URL is not set')
  }

  // Check development-specific settings
  if (import.meta.env.DEV) {
    console.group('🚀 Development Environment Check')
    console.log('API URL:', import.meta.env.VITE_API_URL)
    console.log('Mode:', import.meta.env.MODE)
    console.log('Base URL:', import.meta.env.BASE_URL)
    console.groupEnd()
  }

  // Check backend connectivity
  const checkBackend = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/health`)
      if (!response.ok) {
        issues.push('Backend server is not responding correctly')
      }
    } catch {
      issues.push('Backend server is unreachable')
    }
  }

  return {
    issues,
    checkBackend,
    hasIssues: issues.length > 0
  }
}

// Run environment check on startup
if (import.meta.env.DEV) {
  const envCheck = checkEnvironment()
  
  if (envCheck.hasIssues) {
    console.warn('⚠️ Environment issues detected:', envCheck.issues)
  } else {
    console.log('✅ Environment check passed')
  }
  
  // Check backend connectivity
  envCheck.checkBackend().then(() => {
    console.log('✅ Backend connectivity check completed')
  })
}