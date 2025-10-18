'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

interface Patient {
  id: string
  firstName: string
  lastName: string
  email: string
  phone: string
}

export default function NewAppointment() {
  const [formData, setFormData] = useState({
    patientId: '',
    date: '',
    startTime: '09:00',
    endTime: '10:00',
    type: 'checkup' as const,
    dentist: 'Dr. Johnson',
    notes: '',
    status: 'scheduled' as const
  })
  const [loading, setLoading] = useState(false)
  const [patients, setPatients] = useState<Patient[]>([])
  const [availableSlots, setAvailableSlots] = useState<string[]>([])
  const router = useRouter()

  // Mock data - replace with actual API calls
  useEffect(() => {
    // Fetch patients
    setPatients([
      { id: '1', firstName: 'John', lastName: 'Smith', email: 'john@email.com', phone: '(555) 123-4567' },
      { id: '2', firstName: 'Sarah', lastName: 'Johnson', email: 'sarah@email.com', phone: '(555) 234-5678' },
      { id: '3', firstName: 'Michael', lastName: 'Brown', email: 'michael@email.com', phone: '(555) 345-6789' }
    ])

    // Generate available time slots
    const slots = []
    for (let hour = 9; hour <= 17; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const time = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`
        slots.push(time)
      }
    }
    setAvailableSlots(slots)
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))

    // Auto-set end time based on appointment type
    if (name === 'type' || name === 'startTime') {
      const duration = getAppointmentDuration(value as any)
      const [hours, minutes] = formData.startTime.split(':').map(Number)
      const startDate = new Date(0, 0, 0, hours, minutes)
      const endDate = new Date(startDate.getTime() + duration * 60000)
      const endTime = `${endDate.getHours().toString().padStart(2, '0')}:${endDate.getMinutes().toString().padStart(2, '0')}`
      
      setFormData(prev => ({
        ...prev,
        endTime
      }))
    }
  }

  const getAppointmentDuration = (type: string): number => {
    const durations = {
      checkup: 60,
      cleaning: 60,
      filling: 90,
      crown: 120,
      root_canal: 180,
      other: 60
    }
    return durations[type as keyof typeof durations] || 60
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      // Here you would make an API call to your backend
      console.log('Submitting appointment data:', formData)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Redirect to appointments calendar after successful creation
      router.push('/appointments')
    } catch (error) {
      console.error('Error creating appointment:', error)
    } finally {
      setLoading(false)
    }
  }

  const isFormValid = formData.patientId && formData.date && formData.startTime

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/appointments" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
            ← Back to Appointments
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Schedule New Appointment</h1>
          <p className="text-gray-600 mt-2">Book a new appointment with a patient</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6">
          <div className="space-y-6">
            {/* Patient Selection */}
            <div>
              <label htmlFor="patientId" className="block text-sm font-medium text-gray-700 mb-2">
                Select Patient *
              </label>
              <select
                id="patientId"
                name="patientId"
                required
                value={formData.patientId}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Choose a patient...</option>
                {patients.map(patient => (
                  <option key={patient.id} value={patient.id}>
                    {patient.firstName} {patient.lastName} - {patient.phone}
                  </option>
                ))}
              </select>
            </div>

            {/* Date and Time */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-2">
                  Date *
                </label>
                <input
                  type="date"
                  id="date"
                  name="date"
                  required
                  value={formData.date}
                  onChange={handleChange}
                  min={new Date().toISOString().split('T')[0]}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label htmlFor="startTime" className="block text-sm font-medium text-gray-700 mb-2">
                  Start Time *
                </label>
                <select
                  id="startTime"
                  name="startTime"
                  required
                  value={formData.startTime}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {availableSlots.map(slot => (
                    <option key={slot} value={slot}>
                      {slot}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="endTime" className="block text-sm font-medium text-gray-700 mb-2">
                  End Time
                </label>
                <input
                  type="text"
                  id="endTime"
                  name="endTime"
                  value={formData.endTime}
                  readOnly
                  className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                />
              </div>

              <div>
                <label htmlFor="dentist" className="block text-sm font-medium text-gray-700 mb-2">
                  Dentist *
                </label>
                <select
                  id="dentist"
                  name="dentist"
                  required
                  value={formData.dentist}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Dr. Johnson">Dr. Johnson</option>
                  <option value="Dr. Davis">Dr. Davis</option>
                  <option value="Dr. Wilson">Dr. Wilson</option>
                </select>
              </div>
            </div>

            {/* Appointment Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-2">
                  Appointment Type *
                </label>
                <select
                  id="type"
                  name="type"
                  required
                  value={formData.type}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="checkup">Checkup</option>
                  <option value="cleaning">Cleaning</option>
                  <option value="filling">Filling</option>
                  <option value="crown">Crown</option>
                  <option value="root_canal">Root Canal</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
                  Status *
                </label>
                <select
                  id="status"
                  name="status"
                  required
                  value={formData.status}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="scheduled">Scheduled</option>
                  <option value="confirmed">Confirmed</option>
                </select>
              </div>
            </div>

            {/* Notes */}
            <div>
              <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-2">
                Notes
              </label>
              <textarea
                id="notes"
                name="notes"
                rows={4}
                value={formData.notes}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Add any notes about this appointment..."
              />
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
            <Link
              href="/appointments"
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading || !isFormValid}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Scheduling...' : 'Schedule Appointment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}