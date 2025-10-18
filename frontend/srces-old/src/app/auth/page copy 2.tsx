"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { authService } from "@/services/authService"
import { LoginCredentials, RegisterData } from "@/types/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { UserRole } from "@/types/auth";

export default function AuthPage() {
  const router = useRouter()
  const [isRegister, setIsRegister] = useState(false)

  // Shared error + loading state
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  // Login form
  const [loginData, setLoginData] = useState<LoginCredentials>({
    email: "",
    password: "",
  })

  // Register form
  const [registerData, setRegisterData] = useState<RegisterData>({
    email: "",
    password: "",
    confirmPassword: "",
    first_name: "",
    last_name: "",
    clinic_name: "",
    role: UserRole.VISITOR, // default role
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    if (isRegister) {
      setRegisterData(prev => ({ ...prev, [name]: value }))
    } else {
      setLoginData(prev => ({ ...prev, [name]: value }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    try {
      setLoading(true)
      if (isRegister) {
        if (registerData.password !== registerData.confirmPassword) {
          setError("Passwords do not match")
          return
        }
        await authService.register(registerData)
        setIsRegister(false) // redirect back to login form after success
      } else {
        await authService.login(loginData)
        router.push("/dashboard")
      }
    } catch (err: any) {
      setError(err.message || "Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <Card className="w-full max-w-md p-4">
        <CardHeader>
          <CardTitle>{isRegister ? "Create Account" : "Login"}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {isRegister && (
              <>
                <Input
                  name="first_name"
                  placeholder="First Name"
                  value={registerData.first_name}
                  onChange={handleChange}
                  required
                />
                <Input
                  name="last_name"
                  placeholder="Last Name"
                  value={registerData.last_name}
                  onChange={handleChange}
                  required
                />
              </>
            )}

            <Input
              type="email"
              name="email"
              placeholder="Email"
              value={isRegister ? registerData.email : loginData.email}
              onChange={handleChange}
              required
            />
            <Input
              type="password"
              name="password"
              placeholder="Password"
              value={isRegister ? registerData.password : loginData.password}
              onChange={handleChange}
              required
            />

            {isRegister && (
              <>
                <Input
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm Password"
                  value={registerData.confirmPassword}
                  onChange={handleChange}
                  required
                />
                <Input
                  name="clinic_name"
                  placeholder="Clinic Name (optional)"
                  value={registerData.clinic_name}
                  onChange={handleChange}
                />
                <select
                  name="role"
                  value={registerData.role}
                  onChange={handleChange}
                  className="w-full rounded-md border p-2"
                >
                  <option value="VISITOR">Visitor</option>
                  <option value="ORG_ADMIN">Organization Admin</option>
                </select>
              </>
            )}

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <Button type="submit" disabled={loading} className="w-full">
              {loading
                ? isRegister
                  ? "Registering..."
                  : "Logging in..."
                : isRegister
                ? "Register"
                : "Login"}
            </Button>
          </form>

          <div className="mt-4 text-center">
            <button
              type="button"
              onClick={() => setIsRegister(!isRegister)}
              className="text-blue-500 hover:underline"
            >
              {isRegister
                ? "Already have an account? Login"
                : "Don’t have an account? Register"}
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
