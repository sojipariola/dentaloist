import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Calendar, 
  Search, 
  Plus, 
  Filter,
  Clock,
  User,
  MapPin
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data - will be replaced with real API calls
const mockAppointments = [
  {
    id: 1,
    patient_name: 'John Smith',
    dentist_name: 'Dr. Sarah Johnson',
    start_time: '2024-01-15T09:00:00Z',
    end_time: '2024-01-15T10:00:00Z',
    type: 'Checkup',
    status: 'confirmed',
    treatment_room: 'Room 1'
  },
  {
    id: 2,
    patient_name: 'Emma Wilson',
    dentist_name: 'Dr. Michael Chen',
    start_time: '2024-01-15T10:30:00Z',
    end_time: '2024-01-15T11:30:00Z',
    type: 'Cleaning',
    status: 'confirmed',
    treatment_room: 'Room 2'
  }
]

export default function AppointmentsList() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredAppointments = mockAppointments.filter(apt =>
    apt.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    apt.dentist_name.toLowerCase().includes(searchTerm.toLowerCase())
  ).filter(apt => 
    statusFilter === 'all' || apt.status === statusFilter
  )

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const getStatusColor = (status: string) => {
    const colors = {
      confirmed: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      cancelled: 'bg-red-100 text-red-800',
      completed: 'bg-blue-100 text-blue-800',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Appointments</h1>
          <p className="text-gray-600 mt-2">Manage your appointment schedule</p>
        </div>
        <Button asChild>
          <Link to="/appointments/new">
            <Plus className="h-4 w-4 mr-2" />
            New Appointment
          </Link>
        </Button>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search appointments by patient or dentist..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              icon={Search}
            />
          </div>
          <div className="flex space-x-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="confirmed">Confirmed</option>
              <option value="pending">Pending</option>
              <option value="cancelled">Cancelled</option>
              <option value="completed">Completed</option>
            </select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Appointments List */}
      <Card className="p-0">
        {filteredAppointments.length === 0 ? (
          <div className="p-8 text-center">
            <Calendar className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No appointments found</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || statusFilter !== 'all' 
                ? 'Try adjusting your search or filters' 
                : 'Get started by scheduling your first appointment'
              }
            </p>
            {!(searchTerm || statusFilter !== 'all') && (
              <Button asChild>
                <Link to="/appointments/new">
                  <Plus className="h-4 w-4 mr-2" />
                  Schedule Appointment
                </Link>
              </Button>
            )}
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {filteredAppointments.map((appointment) => (
              <div key={appointment.id} className="p-6 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                        <Calendar className="h-6 w-6 text-primary-600" />
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {appointment.patient_name}
                        </h3>
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(appointment.status)}`}>
                          {appointment.status}
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 mt-1 text-sm text-gray-600">
                        <div className="flex items-center space-x-1">
                          <User className="h-4 w-4" />
                          <span>{appointment.dentist_name}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Clock className="h-4 w-4" />
                          <span>
                            {formatDate(appointment.start_time)} at {formatTime(appointment.start_time)}
                          </span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <MapPin className="h-4 w-4" />
                          <span>{appointment.treatment_room}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button variant="outline" size="sm" asChild>
                      <Link to={`/appointments/${appointment.id}`}>
                        View Details
                      </Link>
                    </Button>
                    <Button variant="outline" size="sm" asChild>
                      <Link to={`/appointments/${appointment.id}/edit`}>
                        Edit
                      </Link>
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}