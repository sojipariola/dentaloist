'use client'
import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

interface Task {
  id: string
  title: string
  description: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  dueDate: string
  assignedTo: string
  category: 'clinical' | 'administrative' | 'maintenance' | 'follow_up' | 'other'
  patientId?: string
  patientName?: string
  createdAt: string
  completedAt?: string
}

interface StaffMember {
  id: string
  name: string
  role: string
}

export default function Tasks() {
  const [activeFilter, setActiveFilter] = useState<'all' | 'pending' | 'in_progress' | 'completed'>('all')
  const [priorityFilter, setPriorityFilter] = useState<'all' | 'low' | 'medium' | 'high' | 'urgent'>('all')
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'clinical' | 'administrative' | 'maintenance' | 'follow_up' | 'other'>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const router = useRouter()

  // Mock data - replace with actual API calls
  const tasks: Task[] = [
    {
      id: '1',
      title: 'Follow up with John Smith',
      description: 'Call patient to check on recovery after filling procedure',
      priority: 'high',
      status: 'pending',
      dueDate: '2024-01-18',
      assignedTo: '2',
      category: 'follow_up',
      patientId: '1',
      patientName: 'John Smith',
      createdAt: '2024-01-15'
    },
    {
      id: '2',
      title: 'Order dental supplies',
      description: 'Restock gloves, masks, and sterilization materials',
      priority: 'medium',
      status: 'in_progress',
      dueDate: '2024-01-20',
      assignedTo: '3',
      category: 'administrative',
      createdAt: '2024-01-14'
    },
    {
      id: '3',
      title: 'Equipment maintenance',
      description: 'Schedule annual maintenance for dental chairs and X-ray machine',
      priority: 'medium',
      status: 'pending',
      dueDate: '2024-01-25',
      assignedTo: '4',
      category: 'maintenance',
      createdAt: '2024-01-13'
    },
    {
      id: '4',
      title: 'Process insurance claims',
      description: 'Submit pending insurance claims for this week\'s procedures',
      priority: 'high',
      status: 'pending',
      dueDate: '2024-01-17',
      assignedTo: '3',
      category: 'administrative',
      createdAt: '2024-01-16'
    },
    {
      id: '5',
      title: 'Patient education materials',
      description: 'Update brochures and handouts for new procedures',
      priority: 'low',
      status: 'completed',
      dueDate: '2024-01-10',
      assignedTo: '2',
      category: 'clinical',
      createdAt: '2024-01-05',
      completedAt: '2024-01-09'
    },
    {
      id: '6',
      title: 'Emergency drill preparation',
      description: 'Prepare and schedule emergency response drill for staff',
      priority: 'urgent',
      status: 'in_progress',
      dueDate: '2024-01-19',
      assignedTo: '1',
      category: 'other',
      createdAt: '2024-01-16'
    }
  ]

  const staff: StaffMember[] = [
    { id: '1', name: 'Dr. Johnson', role: 'Dentist' },
    { id: '2', name: 'Sarah Wilson', role: 'Dental Hygienist' },
    { id: '3', name: 'Mike Chen', role: 'Office Manager' },
    { id: '4', name: 'Emily Davis', role: 'Dental Assistant' }
  ]

  const filteredTasks = tasks.filter(task => {
    const matchesStatus = activeFilter === 'all' || task.status === activeFilter
    const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter
    const matchesCategory = categoryFilter === 'all' || task.category === categoryFilter
    const matchesSearch = searchTerm === '' || 
      task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      task.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (task.patientName && task.patientName.toLowerCase().includes(searchTerm.toLowerCase()))

    return matchesStatus && matchesPriority && matchesCategory && matchesSearch
  })

  const getPriorityBadge = (priority: string) => {
    const priorityColors = {
      low: 'bg-gray-100 text-gray-800',
      medium: 'bg-blue-100 text-blue-800',
      high: 'bg-yellow-100 text-yellow-800',
      urgent: 'bg-red-100 text-red-800'
    }
    return (
      <span className={`text-xs px-2 py-1 rounded-full ${priorityColors[priority as keyof typeof priorityColors]}`}>
        {priority.charAt(0).toUpperCase() + priority.slice(1)}
      </span>
    )
  }

  const getStatusBadge = (status: string) => {
    const statusColors = {
      pending: 'bg-yellow-100 text-yellow-800',
      in_progress: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800'
    }
    return (
      <span className={`text-xs px-2 py-1 rounded-full ${statusColors[status as keyof typeof statusColors]}`}>
        {status.replace('_', ' ').charAt(0).toUpperCase() + status.replace('_', ' ').slice(1)}
      </span>
    )
  }

  const getCategoryBadge = (category: string) => {
    const categoryColors = {
      clinical: 'bg-purple-100 text-purple-800',
      administrative: 'bg-indigo-100 text-indigo-800',
      maintenance: 'bg-orange-100 text-orange-800',
      follow_up: 'bg-pink-100 text-pink-800',
      other: 'bg-gray-100 text-gray-800'
    }
    return (
      <span className={`text-xs px-2 py-1 rounded-full ${categoryColors[category as keyof typeof categoryColors]}`}>
        {category.replace('_', ' ').charAt(0).toUpperCase() + category.replace('_', ' ').slice(1)}
      </span>
    )
  }

  const getAssignedToName = (staffId: string) => {
    const staffMember = staff.find(s => s.id === staffId)
    return staffMember ? staffMember.name : 'Unassigned'
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const isOverdue = (dueDate: string) => {
    return new Date(dueDate) < new Date() && new Date(dueDate) < new Date(new Date().setDate(new Date().getDate() - 1))
  }

  const tasksCount = {
    total: tasks.length,
    pending: tasks.filter(t => t.status === 'pending').length,
    in_progress: tasks.filter(t => t.status === 'in_progress').length,
    completed: tasks.filter(t => t.status === 'completed').length,
    overdue: tasks.filter(t => isOverdue(t.dueDate) && t.status !== 'completed').length
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Tasks & Reminders</h1>
            <p className="text-gray-600 mt-2">Manage practice tasks and staff assignments</p>
          </div>
          <Link
            href="/tasks/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Create Task
          </Link>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-3 bg-gray-100 rounded-lg">
                <span className="text-2xl">📋</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Tasks</p>
                <p className="text-2xl font-bold text-gray-900">{tasksCount.total}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-3 bg-yellow-100 rounded-lg">
                <span className="text-2xl">⏳</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-2xl font-bold text-gray-900">{tasksCount.pending}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 rounded-lg">
                <span className="text-2xl">🚀</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">In Progress</p>
                <p className="text-2xl font-bold text-gray-900">{tasksCount.in_progress}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-3 bg-green-100 rounded-lg">
                <span className="text-2xl">✅</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Completed</p>
                <p className="text-2xl font-bold text-gray-900">{tasksCount.completed}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-3 bg-red-100 rounded-lg">
                <span className="text-2xl">⚠️</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Overdue</p>
                <p className="text-2xl font-bold text-gray-900">{tasksCount.overdue}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
              <select
                value={activeFilter}
                onChange={(e) => setActiveFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Priorities</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Categories</option>
                <option value="clinical">Clinical</option>
                <option value="administrative">Administrative</option>
                <option value="maintenance">Maintenance</option>
                <option value="follow_up">Follow-up</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Tasks List */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Task
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Patient
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Due Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Assigned To
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Priority
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredTasks.map((task) => (
                  <tr key={task.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{task.title}</div>
                        <div className="text-sm text-gray-500">{task.description}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {task.patientName || 'N/A'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      <span className={isOverdue(task.dueDate) ? 'text-red-600 font-medium' : ''}>
                        {formatDate(task.dueDate)}
                        {isOverdue(task.dueDate) && ' (Overdue)'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {getAssignedToName(task.assignedTo)}
                    </td>
                    <td className="px-6 py-4">
                      {getPriorityBadge(task.priority)}
                    </td>
                    <td className="px-6 py-4">
                      {getStatusBadge(task.status)}
                    </td>
                    <td className="px-6 py-4">
                      {getCategoryBadge(task.category)}
                    </td>
                    <td className="px-6 py-4 text-sm font-medium">
                      <div className="flex space-x-2">
                        <button className="text-blue-600 hover:text-blue-900">
                          Edit
                        </button>
                        <button className="text-green-600 hover:text-green-900">
                          Complete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredTasks.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No tasks found matching your criteria.</p>
            </div>
          )}
        </div>

        {/* Upcoming Deadlines */}
        <div className="bg-white rounded-lg shadow p-6 mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Deadlines</h3>
          <div className="space-y-3">
            {tasks
              .filter(task => !isOverdue(task.dueDate) && task.status !== 'completed')
              .sort((a, b) => new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime())
              .slice(0, 5)
              .map(task => (
                <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <div className="text-sm font-medium text-gray-900">{task.title}</div>
                    <div className="text-sm text-gray-500">Due: {formatDate(task.dueDate)}</div>
                  </div>
                  <div className="text-sm text-gray-500">{getAssignedToName(task.assignedTo)}</div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}