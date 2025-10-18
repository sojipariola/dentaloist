import React from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { ArrowLeft, Save } from 'lucide-react'
import { usePatient, useCreatePatient, useUpdatePatient } from '@/api/hooks'
import { Button, Input, Card } from '@/components/ui'
import type { Patient, PatientCreateRequest } from '@/types'

const patientSchema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  email: z.string().email('Please enter a valid email').optional().or(z.literal('')),
  phone: z.string().optional(),
  date_of_birth: z.string().optional(),
  gender: z.string().optional(),
})

type PatientFormData = z.infer<typeof patientSchema>

export default function PatientForm() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEditing = !!id

  const { data: existingPatient } = usePatient(Number(id))
  const createMutation = useCreatePatient()
  const updateMutation = useUpdatePatient()

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<PatientFormData>({
    resolver: zodResolver(patientSchema),
    defaultValues: isEditing && existingPatient ? {
      first_name: existingPatient.first_name,
      last_name: existingPatient.last_name,
      email: existingPatient.email || '',
      phone: existingPatient.phone || '',
      date_of_birth: existingPatient.date_of_birth || '',
      gender: existingPatient.gender || '',
    } : undefined,
  })

  const onSubmit = async (data: PatientFormData) => {
    try {
      const patientData: PatientCreateRequest = {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email || undefined,
        phone: data.phone || undefined,
        date_of_birth: data.date_of_birth || undefined,
        gender: data.gender || undefined,
      }

      if (isEditing && existingPatient) {
        await updateMutation.mutateAsync({
          id: existingPatient.id,
          data: patientData,
        })
      } else {
        await createMutation.mutateAsync(patientData)
      }

      navigate('/patients')
    } catch (error) {
      console.error('Failed to save patient:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" asChild>
            <Link to="/patients">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Patients
            </Link>
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {isEditing ? 'Edit Patient' : 'Add New Patient'}
            </h1>
            <p className="text-gray-600 mt-1">
              {isEditing 
                ? 'Update patient information' 
                : 'Create a new patient record'
              }
            </p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <Card className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Basic Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="First Name *"
                  error={errors.first_name?.message}
                  {...register('first_name')}
                />
                <Input
                  label="Last Name *"
                  error={errors.last_name?.message}
                  {...register('last_name')}
                />
                <Input
                  label="Email"
                  type="email"
                  error={errors.email?.message}
                  {...register('email')}
                />
                <Input
                  label="Phone"
                  type="tel"
                  error={errors.phone?.message}
                  {...register('phone')}
                />
                <Input
                  label="Date of Birth"
                  type="date"
                  error={errors.date_of_birth?.message}
                  {...register('date_of_birth')}
                />
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gender
                  </label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    {...register('gender')}
                  >
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                    <option value="prefer_not_to_say">Prefer not to say</option>
                  </select>
                </div>
              </div>
            </Card>

            {/* Additional sections can be added here for address, emergency contact, etc. */}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
              <div className="space-y-3">
                <Button
                  type="submit"
                  className="w-full"
                  loading={isSubmitting || createMutation.isPending || updateMutation.isPending}
                >
                  <Save className="h-4 w-4 mr-2" />
                  {isEditing ? 'Update Patient' : 'Create Patient'}
                </Button>
                <Button variant="outline" className="w-full" asChild>
                  <Link to="/patients">Cancel</Link>
                </Button>
              </div>
            </Card>

            {/* Form tips */}
            <Card className="p-6 bg-blue-50 border-blue-200">
              <h4 className="text-sm font-medium text-blue-900 mb-2">Form Tips</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Fields marked with * are required</li>
                <li>• Email is used for appointment reminders</li>
                <li>• Phone is used for SMS notifications</li>
                <li>• Complete information helps with patient care</li>
              </ul>
            </Card>
          </div>
        </div>
      </form>
    </div>
  )
}