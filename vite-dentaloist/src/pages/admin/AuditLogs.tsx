import React, { useState } from 'react'
import { 
  FileText, 
  Search,
  Filter,
  Download,
  User,
  Calendar,
  Shield,
  Eye,
  Edit,
  Trash2,
  Plus
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock audit logs
const mockAuditLogs = [
  {
    id: 1,
    user_name: 'Sarah Johnson',
    action: 'user_login',
    description: 'User logged in successfully',
    ip_address: '192.168.1.100',
    user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    timestamp: '2024-01-16T08:30:00Z',
    severity: 'info'
  },
  {
    id: 2,
    user_name: 'Michael Chen',
    action: 'patient_created',
    description: 'Created new patient: John Smith',
    ip_address: '192.168.1.101',
    user_agent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    timestamp: '2024-01-16T09:15:00Z',
    severity: 'info'
  },
  {
    id: 3,
    user_name: 'Jennifer Martinez',
    action: 'appointment_updated',
    description: 'Updated appointment #APT-2024-001',
    ip_address: '192.168.1.102',
    user_agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    timestamp: '2024-01-16T10:30:00Z',
    severity: 'info'
  },
  {
    id: 4,
    user_name: 'Admin User',
    action: 'user_role_changed',
    description: 'Changed role for user Robert Wilson',
    ip_address: '192.168.1.103',
    user_agent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    timestamp: '2024-01-16T11:45:00Z',
    severity: 'warning'
  },
  {
    id: 5,
    user_name: 'Unknown',
    action: 'failed_login',
    description: 'Failed login attempt for user admin',
    ip_address: '203.0.113.1',
    user_agent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    timestamp: '2024-01-16T12:00:00Z',
    severity: 'error'
  }
]

export default function AuditLogs() {
  const [searchTerm, setSearchTerm] = useState('')
  const [actionFilter, setActionFilter] = useState('all')
  const [severityFilter, setSeverityFilter] = useState('all')

  const filteredLogs = mockAuditLogs.filter(log =>
    log.user_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.ip_address.includes(searchTerm)
  ).filter(log => 
    (actionFilter === 'all' || log.action === actionFilter) &&
    (severityFilter === 'all' || log.severity === severityFilter)
  )

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
  }

  const getSeverityColor = (severity: string) => {
    const colors = {
      info: 'bg-blue-100 text-blue-800',
      warning: 'bg-yellow-100 text-yellow-800',
      error: 'bg-red-100 text-red-800',
      success: 'bg-green-100 text-green-800',
    }
    return colors[severity as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  const getActionIcon = (action: string) => {
    const icons: { [key: string]: any } = {
      user_login: Eye,
      user_logout: Eye,
      patient_created: Plus,
      patient_updated: Edit,
      patient_deleted: Trash2,
      appointment_created: Plus,
      appointment_updated: Edit,
      appointment_deleted: Trash2,
      user_role_changed: Shield,
      failed_login: Shield,
    }
    return icons[action] || FileText
  }

  const getActionLabel = (action: string) => {
    const labels: { [key: string]: string } = {
      user_login: 'User Login',
      user_logout: 'User Logout',
      patient_created: 'Patient Created',
      patient_updated: 'Patient Updated',
      patient_deleted: 'Patient Deleted',
      appointment_created: 'Appointment Created',
      appointment_updated: 'Appointment Updated',
      appointment_deleted: 'Appointment Deleted',
      user_role_changed: 'Role Changed',
      failed_login: 'Failed Login',
    }
    return labels[action] || action
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Audit Logs</h1>
          <p className="text-gray-600 mt-2">Monitor system activity and security events</p>
        </div>
        <Button variant="outline">
          <Download className="h-4 w-4 mr-2" />
          Export Logs
        </Button>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search logs by user, description, or IP..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              icon={Search}
            />
          </div>
          <div className="flex flex-wrap gap-2">
            <select
              value={actionFilter}
              onChange={(e) => setActionFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Actions</option>
              <option value="user_login">User Login</option>
              <option value="user_logout">User Logout</option>
              <option value="patient_created">Patient Created</option>
              <option value="patient_updated">Patient Updated</option>
              <option value="appointment_created">Appointment Created</option>
              <option value="appointment_updated">Appointment Updated</option>
              <option value="user_role_changed">Role Changed</option>
              <option value="failed_login">Failed Login</option>
            </select>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Severity</option>
              <option value="info">Info</option>
              <option value="warning">Warning</option>
              <option value="error">Error</option>
              <option value="success">Success</option>
            </select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Audit Logs List */}
      <div className="space-y-4">
        {filteredLogs.map((log) => {
          const ActionIcon = getActionIcon(log.action)
          return (
            <Card key={log.id} className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4">
                  <div className="p-2 bg-gray-100 rounded-lg">
                    <ActionIcon className="h-5 w-5 text-gray-600" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="font-semibold text-gray-900">
                        {getActionLabel(log.action)}
                      </h3>
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(log.severity)}`}>
                        {log.severity}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">{log.description}</p>
                    <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                      <div className="flex items-center space-x-1">
                        <User className="h-4 w-4" />
                        <span>{log.user_name}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Calendar className="h-4 w-4" />
                        <span>{formatDate(log.timestamp)}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Shield className="h-4 w-4" />
                        <span>IP: {log.ip_address}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <Button variant="ghost" size="sm">
                  Details
                </Button>
              </div>
            </Card>
          )
        })}
      </div>

      {filteredLogs.length === 0 && (
        <Card className="p-8 text-center">
          <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No audit logs found</h3>
          <p className="text-gray-600">
            {searchTerm || actionFilter !== 'all' || severityFilter !== 'all'
              ? 'Try adjusting your search or filters'
              : 'No activity has been logged yet'
            }
          </p>
        </Card>
      )}
    </div>
  )
}