import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { 
  ArrowLeft, 
  Edit, 
  Calendar,
  Phone,
  Mail,
  MapPin,
  User
} from 'lucide-react'
import { usePatient } from '@/api/hooks'
import { Button, Card } from '@/components/ui'

export default function PatientDetails() {
  const { id } = useParams<{ id: string }>()
  const { data: patient, isLoading, error } = usePatient(Number(id))

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" asChild>
            <Link to="/patients">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Link>
          </Button>
          <div className="h-8 bg-gray-200 rounded w-48 animate-pulse"></div>
        </div>
        <Card className="p-8">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </Card>
      </div>
    )
  }

  if (error || !patient) {
    return (
      <div className="space-y-6">
        <Button variant="ghost" asChild>
          <Link to="/patients">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Patients
          </Link>
        </Button>
        <Card className="p-8 text-center">
          <div className="text-red-600">
            <p>Failed to load patient details.</p>
            <p className="text-sm mt-2">{error?.message || 'Patient not found'}</p>
          </div>
        </Card>
      </div>
    )
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
              {patient.first_name} {patient.last_name}
            </h1>
            <p className="text-gray-600 mt-1">Patient ID: {patient.public_id}</p>
          </div>
        </div>
        <Button asChild>
          <Link to={`/patients/${patient.id}/edit`}>
            <Edit className="h-4 w-4 mr-2" />
            Edit Patient
          </Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Patient Information */}
        <div className="lg:col-span-2 space-y-6">
          {/* Personal Information */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Personal Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Full Name</label>
                <p className="text-gray-900">{patient.first_name} {patient.last_name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Date of Birth</label>
                <p className="text-gray-900">
                  {patient.date_of_birth 
                    ? new Date(patient.date_of_birth).toLocaleDateString()
                    : '-'
                  }
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Gender</label>
                <p className="text-gray-900">{patient.gender || '-'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Preferred Language</label>
                <p className="text-gray-900">{patient.preferred_language || 'English'}</p>
              </div>
            </div>
          </Card>

          {/* Contact Information */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Contact Information</h2>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Mail className="h-4 w-4 text-gray-400" />
                <span className="text-gray-900">{patient.email || 'No email provided'}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Phone className="h-4 w-4 text-gray-400" />
                <span className="text-gray-900">{patient.phone || 'No phone provided'}</span>
              </div>
              {patient.address && (
                <div className="flex items-start space-x-3">
                  <MapPin className="h-4 w-4 text-gray-400 mt-0.5" />
                  <div>
                    <p className="text-gray-900">
                      {[patient.address.street, patient.address.city, patient.address.state, patient.address.postal_code]
                        .filter(Boolean)
                        .join(', ')}
                    </p>
                    {patient.address.country && (
                      <p className="text-gray-600 text-sm">{patient.address.country}</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          </Card>

          {/* Medical Information */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Medical Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Last Dental Visit</label>
                <p className="text-gray-900">
                  {patient.last_dental_visit
                    ? new Date(patient.last_dental_visit).toLocaleDateString()
                    : 'Never'
                  }
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Next Recall Date</label>
                <p className="text-gray-900">
                  {patient.next_recall_date
                    ? new Date(patient.next_recall_date).toLocaleDateString()
                    : 'Not scheduled'
                  }
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Oral Hygiene</label>
                <p className="text-gray-900">{patient.oral_hygiene || '-'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Status</label>
                <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                  patient.status === 'active' 
                    ? 'bg-green-100 text-green-800'
                    : patient.status === 'inactive'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {patient.status || 'active'}
                </span>
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-2">
              <Button variant="outline" className="w-full justify-start" asChild>
                <Link to={`/appointments/new?patientId=${patient.id}`}>
                  <Calendar className="h-4 w-4 mr-2" />
                  Schedule Appointment
                </Link>
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <User className="h-4 w-4 mr-2" />
                View Medical History
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Edit className="h-4 w-4 mr-2" />
                Add Clinical Note
              </Button>
            </div>
          </Card>

          {/* Emergency Contact */}
          {patient.emergency_contact && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Emergency Contact</h3>
              <div className="space-y-2">
                <div>
                  <p className="font-medium text-gray-900">
                    {patient.emergency_contact.name}
                  </p>
                  <p className="text-sm text-gray-600">
                    {patient.emergency_contact.relationship}
                  </p>
                </div>
                {patient.emergency_contact.phone && (
                  <p className="text-sm text-gray-600">
                    📞 {patient.emergency_contact.phone}
                  </p>
                )}
                {patient.emergency_contact.email && (
                  <p className="text-sm text-gray-600">
                    ✉️ {patient.emergency_contact.email}
                  </p>
                )}
              </div>
            </Card>
          )}

          {/* Insurance Information */}
          {patient.insurance_info && (
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Insurance</h3>
              <div className="space-y-2">
                <div>
                  <p className="font-medium text-gray-900">
                    {patient.insurance_info.provider}
                  </p>
                  <p className="text-sm text-gray-600">
                    Policy: {patient.insurance_info.policy_number}
                  </p>
                </div>
                {patient.insurance_info.group_number && (
                  <p className="text-sm text-gray-600">
                    Group: {patient.insurance_info.group_number}
                  </p>
                )}
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}