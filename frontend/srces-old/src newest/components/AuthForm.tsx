// frontend/components/AuthForm.tsx
"use client";

import { useState } from "react";
import { login, register, googleLogin } from "../app/api/auth";
import { saveTokens } from "../app/lib/auth";
import { useRouter } from "next/navigation";

export default function AuthForm({ mode }: { mode: "login" | "register" }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirst] = useState("");
  const [lastName, setLast] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (mode === "login") {
        const res = await login({ email, password });
        saveTokens(res.data.access_token, res.data.refresh_token);
      } else {
        const res = await register({
          email,
          password,
          first_name: firstName,
          last_name: lastName,
        });
        saveTokens(res.data.access_token, res.data.refresh_token);
      }
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.message || "Something went wrong");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-2xl shadow-md">
      <h1 className="text-2xl font-bold mb-4">
        {mode === "login" ? "Login" : "Register"}
      </h1>
      {error && <p className="text-red-500 mb-3">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        {mode === "register" && (
          <>
            <input
              type="text"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirst(e.target.value)}
              className="w-full border px-3 py-2 rounded-lg"
            />
            <input
              type="text"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLast(e.target.value)}
              className="w-full border px-3 py-2 rounded-lg"
            />
          </>
        )}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border px-3 py-2 rounded-lg"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border px-3 py-2 rounded-lg"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
        >
          {mode === "login" ? "Login" : "Register"}
        </button>
      </form>
      <div className="mt-4">
        <button
          onClick={googleLogin}
          className="w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600"
        >
          Continue with Google
        </button>
      </div>
    </div>
  );
}
