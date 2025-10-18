"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { authService } from "@//services/authService"
import { RegisterData } from "@/types/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { UserRole } from "@/types/auth";

export default function RegisterPage() {
  const router = useRouter()

  const [formData, setFormData] = useState<RegisterData>({
    email: "",
    password: "",
    confirmPassword: "",
    first_name: "",
    last_name: "",
    clinic_name: "",
    role: UserRole.VISITOR, // default role
  })

  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match")
      return
    }

    try {
      setLoading(true)
      await authService.register(formData)
      router.push("/auth/login")
    } catch (err: any) {
      setError(err.message || "Registration failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <Card className="w-full max-w-md p-4">
        <CardHeader>
          <CardTitle>Create Account</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              name="first_name"
              placeholder="First Name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
            <Input
              name="last_name"
              placeholder="Last Name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
            <Input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <Input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <Input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
            <Input
              name="clinic_name"
              placeholder="Clinic Name (optional)"
              value={formData.clinic_name}
              onChange={handleChange}
            />
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="w-full rounded-md border p-2"
            >
              <option value="VISITOR">Visitor</option>
              <option value="ORG_ADMIN">Organization Admin</option>
            </select>

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <Button type="submit" disabled={loading} className="w-full">
              {loading ? "Registering..." : "Register"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
