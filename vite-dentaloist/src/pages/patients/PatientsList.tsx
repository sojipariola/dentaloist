import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Users, 
  Search, 
  Plus, 
  Filter,
  MoreHorizontal,
  Eye,
  Edit,
  Trash2
} from 'lucide-react'
import { usePatients, useDeletePatient } from '@/api/hooks'
import { Button, Input, Card } from '@/components/ui'
import type { PatientFilters } from '@/api/services'

export default function PatientsList() {
  const [filters, setFilters] = useState<PatientFilters>({
    page: 1,
    limit: 10,
    search: '',
    status: '',
  })
  const [showFilters, setShowFilters] = useState(false)

  const { data: patientsData, isLoading, error } = usePatients(filters)
  const deletePatientMutation = useDeletePatient()

  const patients = patientsData?.patients || []
  const totalPages = patientsData?.totalPages || 1

  const handleSearch = (search: string) => {
    setFilters(prev => ({ ...prev, search, page: 1 }))
  }

  const handleStatusFilter = (status: string) => {
    setFilters(prev => ({ ...prev, status: status || undefined, page: 1 }))
  }

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }))
  }

  const handleDeletePatient = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this patient?')) {
      try {
        await deletePatientMutation.mutateAsync(id)
      } catch (error) {
        console.error('Failed to delete patient:', error)
      }
    }
  }

  const formatDate = (dateString?: string) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString()
  }

  const getStatusColor = (status?: string) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      archived: 'bg-red-100 text-red-800',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Patients</h1>
            <p className="text-gray-600 mt-2">Manage your patient records</p>
          </div>
        </div>
        <Card className="p-8 text-center">
          <div className="text-red-600">
            <p>Failed to load patients. Please try again.</p>
            <p className="text-sm mt-2">{error.message}</p>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Patients</h1>
          <p className="text-gray-600 mt-2">Manage your patient records</p>
        </div>
        <Button asChild>
          <Link to="/patients/new">
            <Plus className="h-4 w-4 mr-2" />
            Add Patient
          </Link>
        </Button>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search patients by name, email, or phone..."
              value={filters.search || ''}
              onChange={(e) => handleSearch(e.target.value)}
              icon={Search}
            />
          </div>
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </Button>
        </div>

        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => handleStatusFilter('')}
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  !filters.status 
                    ? 'bg-primary-100 text-primary-800' 
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                }`}
              >
                All
              </button>
              <button
                onClick={() => handleStatusFilter('active')}
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  filters.status === 'active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                }`}
              >
                Active
              </button>
              <button
                onClick={() => handleStatusFilter('inactive')}
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  filters.status === 'inactive'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                }`}
              >
                Inactive
              </button>
            </div>
          </div>
        )}
      </Card>

      {/* Patients Table */}
      <Card className="p-0">
        {isLoading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading patients...</p>
          </div>
        ) : patients.length === 0 ? (
          <div className="p-8 text-center">
            <Users className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No patients found</h3>
            <p className="text-gray-600 mb-4">
              {filters.search || filters.status 
                ? 'Try adjusting your search or filters' 
                : 'Get started by adding your first patient'
              }
            </p>
            {!(filters.search || filters.status) && (
              <Button asChild>
                <Link to="/patients/new">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Patient
                </Link>
              </Button>
            )}
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Patient</th>
                    <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Contact</th>
                    <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Date of Birth</th>
                    <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Status</th>
                    <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Last Visit</th>
                    <th className="text-right py-4 px-6 text-sm font-medium text-gray-900">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {patients.map((patient) => (
                    <tr key={patient.id} className="hover:bg-gray-50">
                      <td className="py-4 px-6">
                        <div>
                          <div className="font-medium text-gray-900">
                            {patient.first_name} {patient.last_name}
                          </div>
                          <div className="text-sm text-gray-500">
                            ID: {patient.public_id}
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="text-sm text-gray-900">{patient.email || '-'}</div>
                        <div className="text-sm text-gray-500">{patient.phone || '-'}</div>
                      </td>
                      <td className="py-4 px-6 text-sm text-gray-900">
                        {formatDate(patient.date_of_birth)}
                      </td>
                      <td className="py-4 px-6">
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(patient.status)}`}>
                          {patient.status || 'active'}
                        </span>
                      </td>
                      <td className="py-4 px-6 text-sm text-gray-900">
                        {formatDate(patient.last_dental_visit)}
                      </td>
                      <td className="py-4 px-6 text-right">
                        <div className="flex justify-end space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            asChild
                          >
                            <Link to={`/patients/${patient.id}`}>
                              <Eye className="h-4 w-4" />
                            </Link>
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            asChild
                          >
                            <Link to={`/patients/${patient.id}/edit`}>
                              <Edit className="h-4 w-4" />
                            </Link>
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeletePatient(patient.id)}
                            disabled={deletePatientMutation.isPending}
                          >
                            <Trash2 className="h-4 w-4 text-red-600" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="px-6 py-4 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-700">
                    Showing page {filters.page} of {totalPages}
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={filters.page === 1}
                      onClick={() => handlePageChange(filters.page! - 1)}
                    >
                      Previous
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={filters.page === totalPages}
                      onClick={() => handlePageChange(filters.page! + 1)}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </Card>
    </div>
  )
}