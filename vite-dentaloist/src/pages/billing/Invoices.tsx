import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  FileText, 
  Plus, 
  Search,
  Filter,
  Download,
  Send,
  MoreHorizontal,
  DollarSign,
  Calendar,
  User
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data
const mockInvoices = [
  {
    id: 1,
    invoice_number: 'INV-2024-001',
    patient_name: 'John Smith',
    amount: 450.00,
    balance_due: 450.00,
    invoice_date: '2024-01-15T00:00:00Z',
    due_date: '2024-02-14T00:00:00Z',
    status: 'pending',
    items: ['Dental Cleaning', 'Examination']
  },
  {
    id: 2,
    invoice_number: 'INV-2024-002',
    patient_name: 'Emma Wilson',
    amount: 1200.00,
    balance_due: 0.00,
    invoice_date: '2024-01-10T00:00:00Z',
    due_date: '2024-02-09T00:00:00Z',
    status: 'paid',
    items: ['Tooth Filling', 'X-rays']
  },
  {
    id: 3,
    invoice_number: 'INV-2024-003',
    patient_name: 'Robert Brown',
    amount: 320.00,
    balance_due: 320.00,
    invoice_date: '2024-01-12T00:00:00Z',
    due_date: '2024-02-11T00:00:00Z',
    status: 'overdue',
    items: ['Consultation']
  }
]

export default function Invoices() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredInvoices = mockInvoices.filter(invoice =>
    invoice.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    invoice.invoice_number.toLowerCase().includes(searchTerm.toLowerCase())
  ).filter(invoice => 
    statusFilter === 'all' || invoice.status === statusFilter
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

  const getStatusColor = (status: string) => {
    const colors = {
      paid: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      overdue: 'bg-red-100 text-red-800',
      draft: 'bg-gray-100 text-gray-800',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  const getStatusText = (status: string) => {
    const texts = {
      paid: 'Paid',
      pending: 'Pending',
      overdue: 'Overdue',
      draft: 'Draft',
    }
    return texts[status as keyof typeof texts] || status
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Invoices</h1>
          <p className="text-gray-600 mt-2">Manage patient invoices and billing</p>
        </div>
        <Button asChild>
          <Link to="/billing/invoices/new">
            <Plus className="h-4 w-4 mr-2" />
            New Invoice
          </Link>
        </Button>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Outstanding</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatCurrency(770.00)}
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pending Invoices</p>
              <p className="text-2xl font-bold text-gray-900">2</p>
            </div>
            <div className="p-3 bg-yellow-100 rounded-lg">
              <FileText className="h-6 w-6 text-yellow-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Overdue</p>
              <p className="text-2xl font-bold text-gray-900">1</p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <Calendar className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Paid This Month</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatCurrency(1200.00)}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search invoices by patient or invoice number..."
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
              <option value="pending">Pending</option>
              <option value="paid">Paid</option>
              <option value="overdue">Overdue</option>
              <option value="draft">Draft</option>
            </select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Invoices Table */}
      <Card className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Invoice</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Patient</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Amount</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Balance Due</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Due Date</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Status</th>
                <th className="text-right py-4 px-6 text-sm font-medium text-gray-900">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredInvoices.map((invoice) => (
                <tr key={invoice.id} className="hover:bg-gray-50">
                  <td className="py-4 px-6">
                    <div>
                      <div className="font-medium text-gray-900">
                        {invoice.invoice_number}
                      </div>
                      <div className="text-sm text-gray-500">
                        {formatDate(invoice.invoice_date)}
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-2">
                      <User className="h-4 w-4 text-gray-400" />
                      <span className="text-gray-900">{invoice.patient_name}</span>
                    </div>
                  </td>
                  <td className="py-4 px-6 text-sm text-gray-900">
                    {formatCurrency(invoice.amount)}
                  </td>
                  <td className="py-4 px-6 text-sm text-gray-900">
                    {formatCurrency(invoice.balance_due)}
                  </td>
                  <td className="py-4 px-6 text-sm text-gray-900">
                    {formatDate(invoice.due_date)}
                  </td>
                  <td className="py-4 px-6">
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(invoice.status)}`}>
                      {getStatusText(invoice.status)}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-right">
                    <div className="flex justify-end space-x-2">
                      <Button variant="ghost" size="sm">
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Send className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" asChild>
                        <Link to={`/billing/invoices/${invoice.id}`}>
                          View
                        </Link>
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredInvoices.length === 0 && (
          <div className="p-8 text-center">
            <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No invoices found</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || statusFilter !== 'all'
                ? 'Try adjusting your search or filters'
                : 'Get started by creating your first invoice'
              }
            </p>
            {!(searchTerm || statusFilter !== 'all') && (
              <Button asChild>
                <Link to="/billing/invoices/new">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Invoice
                </Link>
              </Button>
            )}
          </div>
        )}
      </Card>
    </div>
  )
}