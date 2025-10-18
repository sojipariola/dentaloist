// frontend/src/app/auth/register/page.tsx

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/authService";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { FcGoogle } from "react-icons/fc";
import { FaFacebook, FaGithub } from "react-icons/fa";
import { UserRole } from "@/types/auth";

type Tab = "login" | "register";

export default function AuthPage() {
  const router = useRouter();

  const [activeTab, setActiveTab] = useState<Tab>("login");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Shared state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Registration-only state
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // === Handle Login ===
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await authService.login({ email, password });
      console.log("Login success:", res);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  // === Handle Registration ===
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const res = await authService.register({
        email,
        password,
        confirmPassword,
        first_name: firstName,
        last_name: lastName,
        clinic_name: "Default Clinic", // adjust if needed
        role: UserRole.VISITOR, // default
      });
      console.log("Registration success:", res);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  // === Social Logins ===
  const handleGoogleLogin = () => authService.googleLogin();
  const handleFacebookLogin = () =>
    (window.location.href = "http://127.0.0.1:5000/api/auth/facebook/login");
  const handleGithubLogin = () =>
    (window.location.href = "http://127.0.0.1:5000/api/auth/github/login");

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader>
          <h2 className="text-2xl font-bold text-center">Welcome</h2>
          <p className="text-sm text-gray-500 text-center mt-1">
            Login or create an account
          </p>

          {/* Tabs */}
          <div className="mt-4 flex justify-center space-x-4">
            <button
              onClick={() => setActiveTab("login")}
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                activeTab === "login"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-700"
              }`}
            >
              Login
            </button>
            <button
              onClick={() => setActiveTab("register")}
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                activeTab === "register"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-700"
              }`}
            >
              Register
            </button>
          </div>
        </CardHeader>

        <CardContent>
          {error && (
            <div className="mb-3 text-red-500 text-sm text-center">{error}</div>
          )}

          {/* LOGIN FORM */}
          {activeTab === "login" && (
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  type="email"
                  className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-blue-500"
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
                  className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-blue-500"
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
          )}

          {/* REGISTER FORM */}
          {activeTab === "register" && (
            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  First Name
                </label>
                <input
                  type="text"
                  className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-blue-500"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Last Name
                </label>
                <input
                  type="text"
                  className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-blue-500"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  type="email"
                  className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-blue-500"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <input
                  type="password"
                  className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-blue-500"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Confirm Password
                </label>
                <input
                  type="password"
                  className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-blue-500"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-green-600 text-white rounded-md py-2 hover:bg-green-700 transition disabled:opacity-50"
              >
                {loading ? "Registering..." : "Register"}
              </button>
            </form>
          )}

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
        </CardContent>
      </Card>
    </div>
  );
}

