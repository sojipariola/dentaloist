// src/pages/auth/Register.tsx
import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Eye, EyeOff, UserPlus, Stethoscope } from 'lucide-react'
import { useRegister } from '@/api/hooks'
import { Button, Input, Card } from '@/components/ui'

const registerSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string().min(1, 'Please confirm your password'),
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  organization_id: z.string().optional(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type RegisterFormData = z.infer<typeof registerSchema>

export default function Register() {
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  })

  const registerMutation = useRegister()
  const isLoading = registerMutation.isPending

  const onSubmit = async (data: RegisterFormData) => {
    try {
      const { confirmPassword, ...registerData } = data
      await registerMutation.mutateAsync(registerData)
      navigate('/dashboard', { replace: true })
    } catch (error: any) {
      setError('root', {
        type: 'manual',
        message: error.message || 'Registration failed. Please try again.',
      })
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center items-center space-x-2 mb-6">
            <Stethoscope className="h-8 w-8 text-primary-600" />
            <span className="text-2xl font-bold text-gray-900">Dentaloist</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Or{' '}
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              sign in to your existing account
            </Link>
          </p>
        </div>

        <Card className="p-8">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="First name"
                type="text"
                autoComplete="given-name"
                error={errors.first_name?.message}
                {...register('first_name')}
              />

              <Input
                label="Last name"
                type="text"
                autoComplete="family-name"
                error={errors.last_name?.message}
                {...register('last_name')}
              />
            </div>

            <Input
              label="Email address"
              type="email"
              autoComplete="email"
              error={errors.email?.message}
              {...register('email')}
            />

            <div className="relative">
              <Input
                label="Password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="new-password"
                error={errors.password?.message}
                {...register('password')}
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center mt-6"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4 text-gray-400" />
                ) : (
                  <Eye className="h-4 w-4 text-gray-400" />
                )}
              </button>
            </div>

            <div className="relative">
              <Input
                label="Confirm password"
                type={showConfirmPassword ? 'text' : 'password'}
                autoComplete="new-password"
                error={errors.confirmPassword?.message}
                {...register('confirmPassword')}
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center mt-6"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-4 w-4 text-gray-400" />
                ) : (
                  <Eye className="h-4 w-4 text-gray-400" />
                )}
              </button>
            </div>

            <Input
              label="Organization ID (optional)"
              type="text"
              placeholder="e.g., org_001"
              error={errors.organization_id?.message}
              {...register('organization_id')}
            />

            {errors.root && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="text-sm text-red-700">{errors.root.message}</div>
              </div>
            )}

            <Button
              type="submit"
              variant="primary"
              size="lg"
              loading={isLoading}
              className="w-full"
            >
              <UserPlus className="h-4 w-4 mr-2" />
              Create account
            </Button>
          </form>

          {/* Demo Info */}
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-600 text-center">
              <strong>Note:</strong> Registration requires backend setup.<br />
              For testing, use the login page with demo credentials.
            </p>
          </div>
        </Card>
      </div>
    </div>
  )
}