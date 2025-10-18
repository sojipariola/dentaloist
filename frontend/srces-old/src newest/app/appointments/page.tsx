'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

interface Appointment {
  id: string
  patientId: string
  patientName: string
  patientPhone: string
  date: string
  startTime: string
  endTime: string
  type: 'checkup' | 'cleaning' | 'filling' | 'crown' | 'root_canal' | 'other'
  status: 'scheduled' | 'confirmed' | 'completed' | 'cancelled' | 'no_show'
  notes: string
  dentist: string
}

interface CalendarDay {
  date: Date
  isCurrentMonth: boolean
  isToday: boolean
  appointments: Appointment[]
}

export default function Appointments() {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [view, setView] = useState<'month' | 'week' | 'day'>('month')
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null)
  const router = useRouter()

  // Mock data - replace with actual API call
  const appointments: Appointment[] = [
    {
      id: '1',
      patientId: '1',
      patientName: 'John Smith',
      patientPhone: '(555) 123-4567',
      date: '2024-01-15',
      startTime: '09:00',
      endTime: '10:00',
      type: 'checkup',
      status: 'confirmed',
      notes: 'Routine checkup, last visit was 6 months ago',
      dentist: 'Dr. Johnson'
    },
    {
      id: '2',
      patientId: '2',
      patientName: 'Sarah Johnson',
      patientPhone: '(555) 234-5678',
      date: '2024-01-15',
      startTime: '10:30',
      endTime: '11:30',
      type: 'cleaning',
      status: 'scheduled',
      notes: 'Regular cleaning appointment',
      dentist: 'Dr. Davis'
    },
    {
      id: '3',
      patientId: '3',
      patientName: 'Michael Brown',
      patientPhone: '(555) 345-6789',
      date: '2024-01-16',
      startTime: '14:00',
      endTime: '15:00',
      type: 'filling',
      status: 'confirmed',
      notes: 'Cavity filling on tooth #19',
      dentist: 'Dr. Johnson'
    },
    {
      id: '4',
      patientId: '4',
      patientName: 'Emily Wilson',
      patientPhone: '(555) 456-7890',
      date: '2024-01-18',
      startTime: '11:00',
      endTime: '12:00',
      type: 'crown',
      status: 'scheduled',
      notes: 'Crown placement consultation',
      dentist: 'Dr. Davis'
    }
  ]

  const getAppointmentColor = (type: string) => {
    const colors = {
      checkup: 'bg-blue-100 border-blue-200 text-blue-800',
      cleaning: 'bg-green-100 border-green-200 text-green-800',
      filling: 'bg-yellow-100 border-yellow-200 text-yellow-800',
      crown: 'bg-purple-100 border-purple-200 text-purple-800',
      root_canal: 'bg-red-100 border-red-200 text-red-800',
      other: 'bg-gray-100 border-gray-200 text-gray-800'
    }
    return colors[type as keyof typeof colors] || colors.other
  }

  const getStatusBadge = (status: string) => {
    const statusColors = {
      scheduled: 'bg-gray-100 text-gray-800',
      confirmed: 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
      cancelled: 'bg-red-100 text-red-800',
      no_show: 'bg-orange-100 text-orange-800'
    }
    return (
      <span className={`text-xs px-2 py-1 rounded-full ${statusColors[status as keyof typeof statusColors]}`}>
        {status.replace('_', ' ')}
      </span>
    )
  }

  const generateCalendar = (): CalendarDay[] => {
    const year = currentDate.getFullYear()
    const month = currentDate.getMonth()
    
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const startDate = new Date(firstDay)
    startDate.setDate(startDate.getDate() - startDate.getDay())
    
    const endDate = new Date(lastDay)
    endDate.setDate(endDate.getDate() + (6 - endDate.getDay()))
    
    const calendarDays: CalendarDay[] = []
    const currentDateObj = new Date(startDate)
    
    while (currentDateObj <= endDate) {
      const dateStr = currentDateObj.toISOString().split('T')[0]
      const dayAppointments = appointments.filter(apt => apt.date === dateStr)
      
      calendarDays.push({
        date: new Date(currentDateObj),
        isCurrentMonth: currentDateObj.getMonth() === month,
        isToday: currentDateObj.toDateString() === new Date().toDateString(),
        appointments: dayAppointments
      })
      
      currentDateObj.setDate(currentDateObj.getDate() + 1)
    }
    
    return calendarDays
  }

  const calendarDays = generateCalendar()

  const navigateMonth = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate)
    newDate.setMonth(currentDate.getMonth() + (direction === 'next' ? 1 : -1))
    setCurrentDate(newDate)
  }

  const formatTime = (time: string) => {
    const [hours, minutes] = time.split(':')
    const hour = parseInt(hours)
    return hour > 12 ? `${hour - 12}:${minutes} PM` : `${hour}:${minutes} AM`
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Appointments</h1>
            <p className="text-gray-600 mt-2">Manage your appointment calendar</p>
          </div>
          <Link
            href="/appointments/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Schedule Appointment
          </Link>
        </div>

        {/* Calendar Controls */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              {currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
            </h2>
            
            <div className="flex items-center space-x-4">
              <div className="flex space-x-1">
                <button
                  onClick={() => setView('month')}
                  className={`px-3 py-1 rounded-md ${
                    view === 'month' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
                  }`}
                >
                  Month
                </button>
                <button
                  onClick={() => setView('week')}
                  className={`px-3 py-1 rounded-md ${
                    view === 'week' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
                  }`}
                >
                  Week
                </button>
                <button
                  onClick={() => setView('day')}
                  className={`px-3 py-1 rounded-md ${
                    view === 'day' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
                  }`}
                >
                  Day
                </button>
              </div>
              
              <div className="flex space-x-2">
                <button
                  onClick={() => navigateMonth('prev')}
                  className="p-2 rounded-md bg-gray-200 hover:bg-gray-300"
                >
                  ←
                </button>
                <button
                  onClick={() => setCurrentDate(new Date())}
                  className="px-3 py-1 rounded-md bg-gray-200 hover:bg-gray-300"
                >
                  Today
                </button>
                <button
                  onClick={() => navigateMonth('next')}
                  className="p-2 rounded-md bg-gray-200 hover:bg-gray-300"
                >
                  →
                </button>
              </div>
            </div>
          </div>

          {/* Calendar Grid */}
          <div className="grid grid-cols-7 gap-2 mb-4">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div key={day} className="text-center font-semibold text-gray-700 py-2">
                {day}
              </div>
            ))}
          </div>

          <div className="grid grid-cols-7 gap-2">
            {calendarDays.map((day, index) => (
              <div
                key={index}
                className={`min-h-[120px] p-2 border rounded-lg ${
                  day.isCurrentMonth ? 'bg-white' : 'bg-gray-50'
                } ${day.isToday ? 'border-2 border-blue-500' : 'border-gray-200'}`}
              >
                <div className={`text-sm font-medium ${
                  day.isToday 
                    ? 'bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center' 
                    : day.isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
                }`}>
                  {day.date.getDate()}
                </div>
                
                <div className="mt-2 space-y-1">
                  {day.appointments.slice(0, 3).map(appointment => (
                    <div
                      key={appointment.id}
                      className={`text-xs p-1 rounded border ${getAppointmentColor(appointment.type)} cursor-pointer hover:opacity-80`}
                      onClick={() => setSelectedAppointment(appointment)}
                    >
                      <div className="font-medium truncate">{appointment.patientName}</div>
                      <div className="truncate">{formatTime(appointment.startTime)}</div>
                      <div className="truncate">{appointment.type}</div>
                    </div>
                  ))}
                  
                  {day.appointments.length > 3 && (
                    <div className="text-xs text-gray-500 text-center">
                      +{day.appointments.length - 3} more
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Appointments List */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Appointments</h3>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Date & Time</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Patient</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Type</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Dentist</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Status</th>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {appointments.slice(0, 5).map(appointment => (
                  <tr key={appointment.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <div className="text-sm font-medium text-gray-900">
                        {new Date(appointment.date).toLocaleDateString()}
                      </div>
                      <div className="text-sm text-gray-500">
                        {formatTime(appointment.startTime)} - {formatTime(appointment.endTime)}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="text-sm font-medium text-gray-900">{appointment.patientName}</div>
                      <div className="text-sm text-gray-500">{appointment.patientPhone}</div>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 capitalize">
                      {appointment.type.replace('_', ' ')}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">{appointment.dentist}</td>
                    <td className="px-4 py-3">{getStatusBadge(appointment.status)}</td>
                    <td className="px-4 py-3">
                      <div className="flex space-x-2">
                        <button className="text-blue-600 hover:text-blue-900 text-sm">
                          Edit
                        </button>
                        <button className="text-red-600 hover:text-red-900 text-sm">
                          Cancel
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Appointment Detail Modal */}
        {selectedAppointment && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h3 className="text-lg font-semibold mb-4">Appointment Details</h3>
              
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-700">Patient:</label>
                  <p className="text-gray-900">{selectedAppointment.patientName}</p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-700">Date & Time:</label>
                  <p className="text-gray-900">
                    {new Date(selectedAppointment.date).toLocaleDateString()} •{' '}
                    {formatTime(selectedAppointment.startTime)} - {formatTime(selectedAppointment.endTime)}
                  </p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-700">Type:</label>
                  <p className="text-gray-900 capitalize">{selectedAppointment.type.replace('_', ' ')}</p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-700">Dentist:</label>
                  <p className="text-gray-900">{selectedAppointment.dentist}</p>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-700">Status:</label>
                  <div className="mt-1">{getStatusBadge(selectedAppointment.status)}</div>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-700">Notes:</label>
                  <p className="text-gray-900">{selectedAppointment.notes}</p>
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => setSelectedAppointment(null)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Close
                </button>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                  Edit Appointment
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}