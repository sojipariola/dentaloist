// src/pages/auth/Login.tsx
import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import axios from "axios"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [tenantId, setTenantId] = useState("")

  const mutation = useMutation({
    mutationFn: async () => {
      const res = await axios.post(
        "http://localhost:5000/api/auth/login",
        { email, password },
        {
          headers: tenantId ? { "X-Tenant-ID": tenantId } : {},
        }
      )
      return res.data
    },
    onSuccess: (data) => {
      localStorage.setItem("access_token", data.access_token)
      localStorage.setItem("tenant_id", data.tenant_id)
      alert("Login successful!")
    },
    onError: (err: any) => {
      alert(err.response?.data?.message || "Login failed")
    },
  })

  return (
    <div className="max-w-md mx-auto mt-10 bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Tenant Login</h2>
      <input
        className="w-full border p-2 mb-2"
        placeholder="Tenant ID (optional)"
        value={tenantId}
        onChange={(e) => setTenantId(e.target.value)}
      />
      <input
        className="w-full border p-2 mb-2"
        placeholder="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        className="w-full border p-2 mb-4"
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button
        onClick={() => mutation.mutate()}
        className="w-full bg-blue-600 text-white p-2 rounded"
        disabled={mutation.isPending}
      >
        {mutation.isPending ? "Logging in..." : "Login"}
      </button>
    </div>
  )
}
