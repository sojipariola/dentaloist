import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Stethoscope, 
  Plus, 
  Search,
  Calendar,
  DollarSign,
  Clock,
  User,
  Edit,
  FileText
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data
const mockTreatmentPlans = [
  {
    id: 1,
    patient_name: 'John Smith',
    diagnosis: 'Caries on tooth #19',
    procedures: ['Filling', 'Cleaning'],
    status: 'active',
    estimated_cost: 450,
    created_date: '2024-01-10T00:00:00Z',
    next_appointment: '2024-01-20T14:00:00Z'
  },
  {
    id: 2,
    patient_name: 'Emma Wilson',
    diagnosis: 'Orthodontic consultation',
    procedures: ['Consultation', 'X-rays'],
    status: 'completed',
    estimated_cost: 200,
    created_date: '2024-01-08T00:00:00Z',
    next_appointment: null
  }
]

export default function TreatmentPlans() {
  const [searchTerm, setSearchTerm] = useState('')

  const filteredPlans = mockTreatmentPlans.filter(plan =>
    plan.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    plan.diagnosis.toLowerCase().includes(searchTerm.toLowerCase())
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Treatment Plans</h1>
          <p className="text-gray-600 mt-2">Manage patient treatment plans and procedures</p>
        </div>
        <Button asChild>
          <Link to="/clinical/treatment-plans/new">
            <Plus className="h-4 w-4 mr-2" />
            New Treatment Plan
          </Link>
        </Button>
      </div>

      {/* Search */}
      <Card className="p-6">
        <div className="max-w-md">
          <Input
            placeholder="Search treatment plans..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            icon={Search}
          />
        </div>
      </Card>

      {/* Treatment Plans List */}
      <div className="space-y-4">
        {filteredPlans.map((plan) => (
          <Card key={plan.id} className="p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="p-2 bg-primary-100 rounded-lg">
                    <Stethoscope className="h-5 w-5 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {plan.patient_name}
                    </h3>
                    <div className="flex items-center space-x-4 mt-1">
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(plan.status)}`}>
                        {plan.status}
                      </span>
                      <div className="flex items-center space-x-1 text-sm text-gray-600">
                        <DollarSign className="h-4 w-4" />
                        <span>${plan.estimated_cost}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Diagnosis</label>
                    <p className="text-gray-900">{plan.diagnosis}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Procedures</label>
                    <div className="flex flex-wrap gap-1">
                      {plan.procedures.map((procedure, index) => (
                        <span key={index} className="inline-flex px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                          {procedure}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Created</label>
                    <p className="text-gray-900">{formatDate(plan.created_date)}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Next Appointment</label>
                    <p className="text-gray-900">
                      {plan.next_appointment ? formatDate(plan.next_appointment) : 'Not scheduled'}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <div className="flex items-center space-x-1">
                    <User className="h-4 w-4" />
                    <span>Dr. Sarah Johnson</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Calendar className="h-4 w-4" />
                    <span>Last updated: {formatDate(plan.created_date)}</span>
                  </div>
                </div>
              </div>

              <div className="flex space-x-2 ml-4">
                <Button variant="outline" size="sm" asChild>
                  <Link to={`/clinical/treatment-plans/${plan.id}`}>
                    <FileText className="h-4 w-4 mr-1" />
                    View
                  </Link>
                </Button>
                <Button variant="outline" size="sm">
                  <Edit className="h-4 w-4 mr-1" />
                  Edit
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {filteredPlans.length === 0 && (
        <Card className="p-8 text-center">
          <Stethoscope className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No treatment plans found</h3>
          <p className="text-gray-600 mb-4">
            {searchTerm
              ? 'Try adjusting your search'
              : 'Get started by creating your first treatment plan'
            }
          </p>
          {!searchTerm && (
            <Button asChild>
              <Link to="/clinical/treatment-plans/new">
                <Plus className="h-4 w-4 mr-2" />
                Create Treatment Plan
              </Link>
            </Button>
          )}
        </Card>
      )}
    </div>
  )
}