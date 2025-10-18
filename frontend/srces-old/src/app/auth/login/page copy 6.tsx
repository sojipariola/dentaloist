"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/authService";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { FcGoogle } from "react-icons/fc";
import { FaFacebook, FaGithub } from "react-icons/fa";

export default function LoginPage() {
  const router = useRouter();

  // Form state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // === Email/Password Login ===
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await authService.login({ email, password });
      console.log("Login success:", res);
      router.push("/dashboard"); // redirect to dashboard
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  // === Google Login ===
  const handleGoogleLogin = () => {
    authService.googleLogin();
  };

  // === Facebook Login (placeholder) ===
  const handleFacebookLogin = () => {
    window.location.href = "http://127.0.0.1:5000/api/auth/facebook/login";
  };

  // === GitHub Login (placeholder) ===
  const handleGithubLogin = () => {
    window.location.href = "http://127.0.0.1:5000/api/auth/github/login";
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader>
          <h2 className="text-2xl font-bold text-center">Login</h2>
          <p className="text-sm text-gray-500 text-center mt-1">
            Sign in to your account
          </p>
        </CardHeader>

        <CardContent>
          {/* Error */}
          {error && (
            <div className="mb-3 text-red-500 text-sm text-center">
              {error}
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <input
                type="email"
                className="w-full border rounded-md px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                type="password"
                className="w-full border rounded-md px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white rounded-md py-2 hover:bg-blue-700 transition disabled:opacity-50"
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="mx-2 text-sm text-gray-400">OR</span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>

          {/* Social Logins */}
          <div className="space-y-3">
            <button
              onClick={handleGoogleLogin}
              className="w-full flex items-center justify-center gap-2 border rounded-md py-2 hover:bg-gray-100 transition"
            >
              <FcGoogle size={20} />
              <span>Sign in with Google</span>
            </button>

            <button
              onClick={handleFacebookLogin}
              className="w-full flex items-center justify-center gap-2 border rounded-md py-2 hover:bg-gray-100 transition"
            >
              <FaFacebook size={20} className="text-blue-600" />
              <span>Sign in with Facebook</span>
            </button>

            <button
              onClick={handleGithubLogin}
              className="w-full flex items-center justify-center gap-2 border rounded-md py-2 hover:bg-gray-100 transition"
            >
              <FaGithub size={20} />
              <span>Sign in with GitHub</span>
            </button>
          </div>

          {/* Registration Link */}
          <p className="mt-6 text-center text-sm text-gray-500">
            Don’t have an account?{" "}
            <a
              href="/auth/register"
              className="text-blue-600 hover:underline font-medium"
            >
              Register
            </a>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
