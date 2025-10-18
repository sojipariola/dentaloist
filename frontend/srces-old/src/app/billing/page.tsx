'use client'
import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

interface Invoice {
  id: string
  invoiceNumber: string
  patientId: string
  patientName: string
  date: string
  dueDate: string
  amount: number
  paidAmount: number
  status: 'paid' | 'pending' | 'overdue' | 'partial'
  services: Service[]
  paymentMethod?: string
  paymentDate?: string
}

interface Service {
  id: string
  description: string
  quantity: number
  unitPrice: number
  amount: number
}

interface Payment {
  id: string
  invoiceId: string
  invoiceNumber: string
  patientName: string
  date: string
  amount: number
  method: 'credit_card' | 'debit_card' | 'cash' | 'insurance' | 'online'
  status: 'completed' | 'pending' | 'failed'
  reference: string
}

export default function Billing() {
  const [activeTab, setActiveTab] = useState<'overview' | 'invoices' | 'payments'>('overview')
  const [statusFilter, setStatusFilter] = useState<'all' | 'paid' | 'pending' | 'overdue'>('all')
  const router = useRouter()

  // Mock data - replace with actual API calls
  const invoices: Invoice[] = [
    {
      id: '1',
      invoiceNumber: 'INV-2024-001',
      patientId: '1',
      patientName: 'John Smith',
      date: '2024-01-15',
      dueDate: '2024-02-15',
      amount: 350.00,
      paidAmount: 350.00,
      status: 'paid',
      paymentMethod: 'credit_card',
      paymentDate: '2024-01-16',
      services: [
        { id: '1', description: 'Dental Checkup', quantity: 1, unitPrice: 100.00, amount: 100.00 },
        { id: '2', description: 'Teeth Cleaning', quantity: 1, unitPrice: 150.00, amount: 150.00 },
        { id: '3', description: 'X-Rays', quantity: 1, unitPrice: 100.00, amount: 100.00 }
      ]
    },
    {
      id: '2',
      invoiceNumber: 'INV-2024-002',
      patientId: '2',
      patientName: 'Sarah Johnson',
      date: '2024-01-20',
      dueDate: '2024-02-20',
      amount: 525.00,
      paidAmount: 300.00,
      status: 'partial',
      services: [
        { id: '4', description: 'Cavity Filling', quantity: 2, unitPrice: 150.00, amount: 300.00 },
        { id: '5', description: 'Fluoride Treatment', quantity: 1, unitPrice: 75.00, amount: 75.00 },
        { id: '6', description: 'Night Guard', quantity: 1, unitPrice: 150.00, amount: 150.00 }
      ]
    },
    {
      id: '3',
      invoiceNumber: 'INV-2024-003',
      patientId: '3',
      patientName: 'Michael Brown',
      date: '2024-01-25',
      dueDate: '2024-02-25',
      amount: 1200.00,
      paidAmount: 0.00,
      status: 'pending',
      services: [
        { id: '7', description: 'Dental Crown', quantity: 1, unitPrice: 1200.00, amount: 1200.00 }
      ]
    },
    {
      id: '4',
      invoiceNumber: 'INV-2024-004',
      patientId: '4',
      patientName: 'Emily Wilson',
      date: '2023-12-15',
      dueDate: '2024-01-15',
      amount: 250.00,
      paidAmount: 0.00,
      status: 'overdue',
      services: [
        { id: '8', description: 'Emergency Visit', quantity: 1, unitPrice: 150.00, amount: 150.00 },
        { id: '9', description: 'Medication', quantity: 1, unitPrice: 100.00, amount: 100.00 }
      ]
    }
  ]

  const payments: Payment[] = [
    {
      id: '1',
      invoiceId: '1',
      invoiceNumber: 'INV-2024-001',
      patientName: 'John Smith',
      date: '2024-01-16',
      amount: 350.00,
      method: 'credit_card',
      status: 'completed',
      reference: 'CHG-123456'
    },
    {
      id: '2',
      invoiceId: '2',
      invoiceNumber: 'INV-2024-002',
      patientName: 'Sarah Johnson',
      date: '2024-01-22',
      amount: 300.00,
      method: 'debit_card',
      status: 'completed',
      reference: 'CHG-123457'
    },
    {
      id: '3',
      invoiceId: '5',
      invoiceNumber: 'INV-2024-005',
      patientName: 'David Lee',
      date: '2024-01-18',
      amount: 200.00,
      method: 'insurance',
      status: 'pending',
      reference: 'INS-789012'
    }
  ]

  const filteredInvoices = invoices.filter(invoice => 
    statusFilter === 'all' || invoice.status === statusFilter
  )

  const totalRevenue = invoices.reduce((sum, inv) => sum + inv.paidAmount, 0)
  const pendingAmount = invoices.reduce((sum, inv) => sum + (inv.amount - inv.paidAmount), 0)
  const overdueAmount = invoices
    .filter(inv => inv.status === 'overdue')
    .reduce((sum, inv) => sum + (inv.amount - inv.paidAmount), 0)

  const getStatusBadge = (status: string) => {
    const statusColors = {
      paid: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      overdue: 'bg-red-100 text-red-800',
      partial: 'bg-blue-100 text-blue-800'
    }
    return (
      <span className={`text-xs px-2 py-1 rounded-full ${statusColors[status as keyof typeof statusColors]}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    )
  }

  const getPaymentMethodBadge = (method?: string) => {
    if (!method) return null
    const methodText = {
      credit_card: 'Credit Card',
      debit_card: 'Debit Card',
      cash: 'Cash',
      insurance: 'Insurance',
      online: 'Online'
    }
    return (
      <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-800">
        {methodText[method as keyof typeof methodText]}
      </span>
    )
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const isOverdue = (dueDate: string) => {
    return new Date(dueDate) < new Date() && new Date(dueDate) < new Date(new Date().setDate(new Date().getDate() - 1))
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Billing & Payments</h1>
            <p className="text-gray-600 mt-2">Manage invoices, payments, and financial reports</p>
          </div>
          <Link
            href="/billing/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Create Invoice
          </Link>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow mb-8">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview', icon: '📊' },
              { id: 'invoices', label: 'Invoices', icon: '🧾' },
              { id: 'payments', label: 'Payments', icon: '💳' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow p-6">
          {activeTab === 'overview' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Financial Overview</h2>
              
              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-green-50 rounded-lg p-6">
                  <div className="flex items-center">
                    <div className="p-3 bg-green-100 rounded-lg">
                      <span className="text-2xl">💰</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                      <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalRevenue)}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-yellow-50 rounded-lg p-6">
                  <div className="flex items-center">
                    <div className="p-3 bg-yellow-100 rounded-lg">
                      <span className="text-2xl">⏰</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Pending Payments</p>
                      <p className="text-2xl font-bold text-gray-900">{formatCurrency(pendingAmount)}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-red-50 rounded-lg p-6">
                  <div className="flex items-center">
                    <div className="p-3 bg-red-100 rounded-lg">
                      <span className="text-2xl">⚠️</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Overdue Amount</p>
                      <p className="text-2xl font-bold text-gray-900">{formatCurrency(overdueAmount)}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Invoices */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Invoices</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Invoice #</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Patient</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Date</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Amount</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {invoices.slice(0, 5).map(invoice => (
                        <tr key={invoice.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3 text-sm font-medium text-gray-900">{invoice.invoiceNumber}</td>
                          <td className="px-4 py-3 text-sm text-gray-900">{invoice.patientName}</td>
                          <td className="px-4 py-3 text-sm text-gray-900">{formatDate(invoice.date)}</td>
                          <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(invoice.amount)}</td>
                          <td className="px-4 py-3">{getStatusBadge(invoice.status)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Recent Payments */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Payments</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Date</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Patient</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Invoice #</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Amount</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Method</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {payments.slice(0, 5).map(payment => (
                        <tr key={payment.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3 text-sm text-gray-900">{formatDate(payment.date)}</td>
                          <td className="px-4 py-3 text-sm text-gray-900">{payment.patientName}</td>
                          <td className="px-4 py-3 text-sm text-gray-900">{payment.invoiceNumber}</td>
                          <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(payment.amount)}</td>
                          <td className="px-4 py-3">{getPaymentMethodBadge(payment.method)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'invoices' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Invoices</h2>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value as any)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">All Status</option>
                  <option value="paid">Paid</option>
                  <option value="pending">Pending</option>
                  <option value="overdue">Overdue</option>
                </select>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Invoice #</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Patient</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Date</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Due Date</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Amount</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Paid</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Balance</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Status</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {filteredInvoices.map(invoice => (
                      <tr key={invoice.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">{invoice.invoiceNumber}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{invoice.patientName}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{formatDate(invoice.date)}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">
                          <span className={isOverdue(invoice.dueDate) ? 'text-red-600' : ''}>
                            {formatDate(invoice.dueDate)}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(invoice.amount)}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(invoice.paidAmount)}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">
                          {formatCurrency(invoice.amount - invoice.paidAmount)}
                        </td>
                        <td className="px-4 py-3">{getStatusBadge(invoice.status)}</td>
                        <td className="px-4 py-3">
                          <div className="flex space-x-2">
                            <button className="text-blue-600 hover:text-blue-900 text-sm">
                              View
                            </button>
                            <button className="text-green-600 hover:text-green-900 text-sm">
                              Payment
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'payments' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Payment History</h2>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Date</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Patient</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Invoice #</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Amount</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Method</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Reference</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {payments.map(payment => (
                      <tr key={payment.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm text-gray-900">{formatDate(payment.date)}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{payment.patientName}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{payment.invoiceNumber}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(payment.amount)}</td>
                        <td className="px-4 py-3">{getPaymentMethodBadge(payment.method)}</td>
                        <td className="px-4 py-3 text-sm text-gray-900">{payment.reference}</td>
                        <td className="px-4 py-3">
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            payment.status === 'completed' 
                              ? 'bg-green-100 text-green-800' 
                              : payment.status === 'pending'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {payment.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}