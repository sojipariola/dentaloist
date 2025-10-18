// frontend/src/components/ErrorBoundary.tsx
'use client';

import React from 'react';

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorMessage: string;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null,
      errorMessage: '' 
    };
  }

  static getDerivedStateFromError(error: any): ErrorBoundaryState {
    // Extract the error message safely
    let errorMessage = 'An unexpected error occurred';
    
    if (typeof error === 'string') {
      errorMessage = error;
    } else if (error instanceof Error) {
      errorMessage = error.message;
    } else if (error && typeof error === 'object') {
      // Handle error objects with message property
      if (error.message) {
        errorMessage = error.message;
      } else if (error.error) {
        errorMessage = error.error;
      } else {
        // Stringify the object for debugging
        errorMessage = JSON.stringify(error, null, 2);
      }
    }
    
    return { 
      hasError: true, 
      error: error instanceof Error ? error : null,
      errorMessage 
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-red-600 mb-4">Something went wrong</h2>
            <pre className="text-gray-700 mb-4 whitespace-pre-wrap text-sm">
              {this.state.errorMessage}
            </pre>
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              onClick={() => this.setState({ 
                hasError: false, 
                error: null,
                errorMessage: '' 
              })}
            >
              Try again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;