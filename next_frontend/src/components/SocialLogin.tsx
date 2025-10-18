'use client';

export default function SocialLogin() {
  const handleSocialLogin = (provider: 'google' | 'facebook' | 'github') => {
    // Redirect directly to Flask backend OAuth route
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/auth/${provider}`;
  };

  return (
    <div className="flex flex-col items-center space-y-3 mt-6">
      <button
        onClick={() => handleSocialLogin('google')}
        className="w-64 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
      >
        Continue with Google
      </button>

      <button
        onClick={() => handleSocialLogin('facebook')}
        className="w-64 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Continue with Facebook
      </button>

      <button
        onClick={() => handleSocialLogin('github')}
        className="w-64 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900"
      >
        Continue with GitHub
      </button>
    </div>
  );
}
// next_frontend/src/components/SocialLogin.tsx --- IGNORE ---