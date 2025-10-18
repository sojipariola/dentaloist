'use client'

import LoginForm from '@/components/forms/LoginForm'

export default function LoginPage() {
  return (
    <section className="container mx-auto px-6 py-20">
      <h1 className="text-3xl font-bold mb-6">Login</h1>
      <LoginForm />
    </section>
  )
}
