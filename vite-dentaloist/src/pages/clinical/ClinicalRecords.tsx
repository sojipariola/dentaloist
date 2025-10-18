import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  FileText, 
  Search, 
  Plus, 
  Filter,
  Stethoscope,
  Pill,
  AlertTriangle,
  Calendar,
  User
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data - will be replaced with real API calls
const mockClinicalRecords = [
  {
    id: 1,
    patient_name: 'John Smith',
    record_type: 'Treatment Plan',
    created_by: 'Dr. Sarah Johnson',
    created_at: '2024-01-10T14:30:00Z',
    status: 'active',
    priority: 'high'
  },
  {
    id: 2,
    patient_name: 'Emma Wilson',
    record_type: 'Clinical Note',
    created_by: 'Dr. Michael Chen',
    created_at: '2024-01-12T10:15:00Z',
    status: 'completed',
    priority: 'medium'
  },
  {
    id: 3,
    patient_name: 'Robert Brown',
    record_type: 'Prescription',
    created_by: 'Dr. Sarah Johnson',
    created_at: '2024-01-14T16:45:00Z',
    status: 'active',
    priority: 'high'
  }
]

export default function ClinicalRecords() {
  const [searchTerm, setSearchTerm] = useState('')
  const [typeFilter, setTypeFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredRecords = mockClinicalRecords.filter(record =>
    record.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.record_type.toLowerCase().includes(searchTerm.toLowerCase())
  ).filter(record => 
    (typeFilter === 'all' || record.record_type === typeFilter) &&
    (statusFilter === 'all' || record.status === statusFilter)
  )

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const getStatusColor = (status: string) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
      draft: 'bg-gray-100 text-gray-800',
      cancelled: 'bg-red-100 text-red-800',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  const getPriorityColor = (priority: string) => {
    const colors = {
      high: 'text-red-600',
      medium: 'text-yellow-600',
      low: 'text-green-600',
    }
    return colors[priority as keyof typeof colors] || 'text-gray-600'
  }

  const getRecordIcon = (type: string) => {
    const icons = {
      'Treatment Plan': Stethoscope,
      'Clinical Note': FileText,
      'Prescription': Pill,
      'Allergy': AlertTriangle,
    }
    return icons[type as keyof typeof icons] || FileText
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Clinical Records</h1>
          <p className="text-gray-600 mt-2">Manage patient clinical documentation</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" asChild>
            <Link to="/clinical/treatment-plans/new">
              <Stethoscope className="h-4 w-4 mr-2" />
              Treatment Plan
            </Link>
          </Button>
          <Button asChild>
            <Link to="/clinical/notes/new">
              <Plus className="h-4 w-4 mr-2" />
              Clinical Note
            </Link>
          </Button>
        </div>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search records by patient name or type..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              icon={Search}
            />
          </div>
          <div className="flex flex-wrap gap-2">
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="Treatment Plan">Treatment Plans</option>
              <option value="Clinical Note">Clinical Notes</option>
              <option value="Prescription">Prescriptions</option>
              <option value="Allergy">Allergies</option>
            </select>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="draft">Draft</option>
            </select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Clinical Records Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredRecords.map((record) => {
          const IconComponent = getRecordIcon(record.record_type)
          return (
            <Card key={record.id} className="p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-primary-100 rounded-lg">
                    <IconComponent className="h-5 w-5 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{record.record_type}</h3>
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(record.status)}`}>
                      {record.status}
                    </span>
                  </div>
                </div>
                <div className={`${getPriorityColor(record.priority)}`}>
                  {record.priority === 'high' && <AlertTriangle className="h-4 w-4" />}
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <User className="h-4 w-4" />
                  <span>{record.patient_name}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Calendar className="h-4 w-4" />
                  <span>{formatDate(record.created_at)}</span>
                </div>
                <div className="text-sm text-gray-600">
                  By: {record.created_by}
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm" className="flex-1" asChild>
                    <Link to={`/clinical/records/${record.id}`}>
                      View Details
                    </Link>
                  </Button>
                  <Button variant="outline" size="sm">
                    Edit
                  </Button>
                </div>
              </div>
            </Card>
          )
        })}
      </div>

      {filteredRecords.length === 0 && (
        <Card className="p-8 text-center">
          <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No clinical records found</h3>
          <p className="text-gray-600 mb-4">
            {searchTerm || typeFilter !== 'all' || statusFilter !== 'all'
              ? 'Try adjusting your search or filters'
              : 'Get started by creating your first clinical record'
            }
          </p>
          {!(searchTerm || typeFilter !== 'all' || statusFilter !== 'all') && (
            <Button asChild>
              <Link to="/clinical/notes/new">
                <Plus className="h-4 w-4 mr-2" />
                Create Clinical Note
              </Link>
            </Button>
          )}
        </Card>
      )}
    </div>
  )
}