// src/app/not-found.tsx (without lucide-react)
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center p-8 bg-white rounded-2xl shadow-xl max-w-md">
        <div className="text-9xl font-bold text-blue-600 mb-4">404</div>
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Oops! Page not found</h1>
        <p className="text-gray-600 mb-6">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link 
          href="/"
          className="inline-flex items-center justify-center bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Return to Home
        </Link>
      </div>
    </div>
  )
}