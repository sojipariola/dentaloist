import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  CreditCard, 
  Plus, 
  Search,
  Filter,
  Download,
  CheckCircle,
  XCircle,
  Calendar,
  User,
  DollarSign
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data
const mockPayments = [
  {
    id: 1,
    payment_number: 'PAY-2024-001',
    patient_name: 'Emma Wilson',
    amount: 1200.00,
    payment_method: 'Credit Card',
    payment_date: '2024-01-12T10:30:00Z',
    status: 'completed',
    invoice_number: 'INV-2024-002'
  },
  {
    id: 2,
    payment_number: 'PAY-2024-002',
    patient_name: 'John Smith',
    amount: 200.00,
    payment_method: 'Cash',
    payment_date: '2024-01-16T14:15:00Z',
    status: 'completed',
    invoice_number: 'INV-2024-001'
  },
  {
    id: 3,
    payment_number: 'PAY-2024-003',
    patient_name: 'Robert Brown',
    amount: 150.00,
    payment_method: 'Insurance',
    payment_date: '2024-01-18T11:00:00Z',
    status: 'pending',
    invoice_number: 'INV-2024-004'
  }
]

export default function Payments() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredPayments = mockPayments.filter(payment =>
    payment.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    payment.payment_number.toLowerCase().includes(searchTerm.toLowerCase())
  ).filter(payment => 
    statusFilter === 'all' || payment.status === statusFilter
  )

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount)
  }

  const getStatusIcon = (status: string) => {
    return status === 'completed' ? 
      <CheckCircle className="h-4 w-4 text-green-500" /> :
      <XCircle className="h-4 w-4 text-yellow-500" />
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Payments</h1>
          <p className="text-gray-600 mt-2">Manage patient payments and transactions</p>
        </div>
        <Button asChild>
          <Link to="/billing/payments/new">
            <Plus className="h-4 w-4 mr-2" />
            Record Payment
          </Link>
        </Button>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search payments by patient or payment number..."
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
              <option value="completed">Completed</option>
              <option value="pending">Pending</option>
              <option value="failed">Failed</option>
            </select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Payments List */}
      <div className="grid grid-cols-1 gap-4">
        {filteredPayments.map((payment) => (
          <Card key={payment.id} className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <CreditCard className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {payment.payment_number}
                    </h3>
                    {getStatusIcon(payment.status)}
                  </div>
                  <div className="flex items-center space-x-4 mt-1 text-sm text-gray-600">
                    <div className="flex items-center space-x-1">
                      <User className="h-4 w-4" />
                      <span>{payment.patient_name}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Calendar className="h-4 w-4" />
                      <span>{formatDate(payment.payment_date)}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <DollarSign className="h-4 w-4" />
                      <span>{formatCurrency(payment.amount)}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-right">
                <div className="text-sm text-gray-600 mb-1">{payment.payment_method}</div>
                <div className="text-lg font-semibold text-gray-900">
                  {formatCurrency(payment.amount)}
                </div>
                <div className="text-sm text-gray-500">
                  Invoice: {payment.invoice_number}
                </div>
              </div>

              <div className="flex space-x-2">
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-1" />
                  Receipt
                </Button>
                <Button variant="outline" size="sm" asChild>
                  <Link to={`/billing/payments/${payment.id}`}>
                    View Details
                  </Link>
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {filteredPayments.length === 0 && (
        <Card className="p-8 text-center">
          <CreditCard className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No payments found</h3>
          <p className="text-gray-600 mb-4">
            {searchTerm || statusFilter !== 'all'
              ? 'Try adjusting your search or filters'
              : 'No payments have been recorded yet'
            }
          </p>
          {!(searchTerm || statusFilter !== 'all') && (
            <Button asChild>
              <Link to="/billing/payments/new">
                <Plus className="h-4 w-4 mr-2" />
                Record Payment
              </Link>
            </Button>
          )}
        </Card>
      )}
    </div>
  )
}