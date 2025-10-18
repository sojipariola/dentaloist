// src/pages/auth/Register.tsx
import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import axios from "axios"

export default function Register() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [organizationName, setOrganizationName] = useState("")

  const mutation = useMutation({
    mutationFn: async () => {
      const res = await axios.post("http://localhost:5000/api/auth/register", {
        email,
        password,
        organization_name: organizationName,
      })
      return res.data
    },
    onSuccess: (data) => {
      localStorage.setItem("access_token", data.access_token)
      localStorage.setItem("tenant_id", data.tenant_id)
      alert("Registration successful!")
    },
    onError: (err: any) => {
      alert(err.response?.data?.message || "Registration failed")
    },
  })

  return (
    <div className="max-w-md mx-auto mt-10 bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Create Tenant Account</h2>
      <input
        className="w-full border p-2 mb-2"
        placeholder="Organization Name"
        value={organizationName}
        onChange={(e) => setOrganizationName(e.target.value)}
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
        className="w-full bg-green-600 text-white p-2 rounded"
        disabled={mutation.isPending}
      >
        {mutation.isPending ? "Registering..." : "Register"}
      </button>
    </div>
  )
}
