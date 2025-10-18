'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

interface Patient {
  id: string
  firstName: string
  lastName: string
}

interface StaffMember {
  id: string
  name: string
  role: string
}

export default function NewTask() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium' as 'low' | 'medium' | 'high' | 'urgent',
    dueDate: '',
    assignedTo: '',
    category: 'other' as 'clinical' | 'administrative' | 'maintenance' | 'follow_up' | 'other',
    patientId: '',
    status: 'pending' as 'pending' | 'in_progress' | 'completed' | 'cancelled'
  })
  const [patients, setPatients] = useState<Patient[]>([])
  const [staff, setStaff] = useState<StaffMember[]>([])
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  // Mock data - replace with actual API calls
  useEffect(() => {
    setPatients([
      { id: '1', firstName: 'John', lastName: 'Smith' },
      { id: '2', firstName: 'Sarah', lastName: 'Johnson' },
      { id: '3', firstName: 'Michael', lastName: 'Brown' },
      { id: '4', firstName: 'Emily', lastName: 'Wilson' }
    ])

    setStaff([
      { id: '1', name: 'Dr. Johnson', role: 'Dentist' },
      { id: '2', name: 'Sarah Wilson', role: 'Dental Hygienist' },
      { id: '3', name: 'Mike Chen', role: 'Office Manager' },
      { id: '4', name: 'Emily Davis', role: 'Dental Assistant' }
    ])
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      // Here you would make an API call to your backend
      const taskData = {
        ...formData,
        createdAt: new Date().toISOString(),
        patientName: formData.patientId 
          ? patients.find(p => p.id === formData.patientId)?.firstName + ' ' + 
            patients.find(p => p.id === formData.patientId)?.lastName
          : undefined
      }

      console.log('Submitting task data:', taskData)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      router.push('/tasks')
    } catch (error) {
      console.error('Error creating task:', error)
    } finally {
      setLoading(false)
    }
  }

  const isFormValid = formData.title && formData.dueDate && formData.assignedTo

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/tasks" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
            ← Back to Tasks
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Create New Task</h1>
          <p className="text-gray-600 mt-2">Assign a new task to your team</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6">
          <div className="space-y-6">
            {/* Basic Information */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Task Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                required
                value={formData.title}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter task title..."
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                rows={4}
                value={formData.description}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Describe the task in detail..."
              />
            </div>

            {/* Task Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                  Priority *
                </label>
                <select
                  id="priority"
                  name="priority"
                  required
                  value={formData.priority}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>

              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                  Category *
                </label>
                <select
                  id="category"
                  name="category"
                  required
                  value={formData.category}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="clinical">Clinical</option>
                  <option value="administrative">Administrative</option>
                  <option value="maintenance">Maintenance</option>
                  <option value="follow_up">Follow-up</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-2">
                  Due Date *
                </label>
                <input
                  type="date"
                  id="dueDate"
                  name="dueDate"
                  required
                  value={formData.dueDate}
                  onChange={handleChange}
                  min={new Date().toISOString().split('T')[0]}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
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
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                </select>
              </div>
            </div>

            {/* Assignment */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="assignedTo" className="block text-sm font-medium text-gray-700 mb-2">
                  Assign To *
                </label>
                <select
                  id="assignedTo"
                  name="assignedTo"
                  required
                  value={formData.assignedTo}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select staff member...</option>
                  {staff.map(member => (
                    <option key={member.id} value={member.id}>
                      {member.name} ({member.role})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="patientId" className="block text-sm font-medium text-gray-700 mb-2">
                  Related Patient (Optional)
                </label>
                <select
                  id="patientId"
                  name="patientId"
                  value={formData.patientId}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select patient...</option>
                  {patients.map(patient => (
                    <option key={patient.id} value={patient.id}>
                      {patient.firstName} {patient.lastName}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
            <Link
              href="/tasks"
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading || !isFormValid}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating Task...' : 'Create Task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}