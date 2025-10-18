"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { authService } from "@/services/authService"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { FcGoogle } from "react-icons/fc"
import { FaFacebook } from "react-icons/fa"
import { UserRole } from "@/types/auth";

type Mode = "login" | "register"

export default function AuthPage() {
  const [mode, setMode] = useState<Mode>("login")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirmPassword: "",
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      if (mode === "login") {
        await authService.login({
          email: form.email,
          password: form.password,
        })
      } else {
        if (form.password !== form.confirmPassword) {
          setError("Passwords do not match")
          setLoading(false)
          return
        }

        await authService.register({
          email: form.email,
          password: form.password,
          confirmPassword: form.confirmPassword,
          first_name: form.first_name,
          last_name: form.last_name,
          clinic_name: "", // optional, depends on backend
          role: UserRole.VISITOR, // adjust default role
        })
      }

      router.push("/dashboard")
    } catch (err: any) {
      setError(err.message || "Authentication failed")
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleLogin = () => {
    authService.googleLogin()
  }

  const handleFacebookLogin = () => {
    if (typeof window !== "undefined") {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/facebook/login`
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>
            {mode === "login" ? "Sign in to your account" : "Create your account"}
          </CardTitle>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <>
                <Input
                  type="text"
                  name="first_name"
                  placeholder="First Name"
                  value={form.first_name}
                  onChange={handleChange}
                  required
                />
                <Input
                  type="text"
                  name="last_name"
                  placeholder="Last Name"
                  value={form.last_name}
                  onChange={handleChange}
                  required
                />
              </>
            )}

            <Input
              type="email"
              name="email"
              placeholder="Email"
              value={form.email}
              onChange={handleChange}
              required
            />

            <Input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              required
            />

            {mode === "register" && (
              <Input
                type="password"
                name="confirmPassword"
                placeholder="Confirm Password"
                value={form.confirmPassword}
                onChange={handleChange}
                required
              />
            )}

            {error && <p className="text-sm text-red-500">{error}</p>}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Please wait..." : mode === "login" ? "Login" : "Register"}
            </Button>
          </form>
        </CardContent>

        <CardFooter className="flex flex-col space-y-3">
          <div className="flex w-full items-center space-x-2">
            <div className="h-px flex-1 bg-gray-300" />
            <span className="text-xs text-gray-500">OR</span>
            <div className="h-px flex-1 bg-gray-300" />
          </div>

          {/* Social logins */}
          <Button
            type="button"
            variant="outline"
            className="w-full flex items-center justify-center space-x-2"
            onClick={handleGoogleLogin}
          >
            <FcGoogle size={20} />
            <span>Continue with Google</span>
          </Button>

          <Button
            type="button"
            variant="outline"
            className="w-full flex items-center justify-center space-x-2 text-blue-600"
            onClick={handleFacebookLogin}
          >
            <FaFacebook size={20} />
            <span>Continue with Facebook</span>
          </Button>

          {/* Toggle login/register */}
          <p className="text-sm text-gray-600 text-center">
            {mode === "login" ? (
              <>
                Don’t have an account?{" "}
                <button
                  type="button"
                  className="text-blue-600 hover:underline"
                  onClick={() => setMode("register")}
                >
                  Register
                </button>
              </>
            ) : (
              <>
                Already have an account?{" "}
                <button
                  type="button"
                  className="text-blue-600 hover:underline"
                  onClick={() => setMode("login")}
                >
                  Login
                </button>
              </>
            )}
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}
