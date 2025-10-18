'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

interface Patient {
  id: string
  firstName: string
  lastName: string
  email: string
  phone: string
}

interface Service {
  id: string
  description: string
  price: number
  category: string
}

export default function NewInvoice() {
  const [formData, setFormData] = useState({
    patientId: '',
    date: new Date().toISOString().split('T')[0],
    dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    services: [] as Array<{
      serviceId: string
      description: string
      quantity: number
      unitPrice: number
      amount: number
    }>,
    notes: '',
    terms: 'Net 30',
    status: 'pending' as const
  })
  const [patients, setPatients] = useState<Patient[]>([])
  const [services, setServices] = useState<Service[]>([])
  const [selectedService, setSelectedService] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  // Mock data - replace with actual API calls
  useEffect(() => {
    setPatients([
      { id: '1', firstName: 'John', lastName: 'Smith', email: 'john@email.com', phone: '(555) 123-4567' },
      { id: '2', firstName: 'Sarah', lastName: 'Johnson', email: 'sarah@email.com', phone: '(555) 234-5678' },
      { id: '3', firstName: 'Michael', lastName: 'Brown', email: 'michael@email.com', phone: '(555) 345-6789' }
    ])

    setServices([
      { id: '1', description: 'Dental Checkup', price: 100.00, category: 'Examination' },
      { id: '2', description: 'Teeth Cleaning', price: 150.00, category: 'Hygiene' },
      { id: '3', description: 'X-Rays', price: 100.00, category: 'Diagnostic' },
      { id: '4', description: 'Cavity Filling', price: 150.00, category: 'Restorative' },
      { id: '5', description: 'Crown', price: 1200.00, category: 'Restorative' },
      { id: '6', description: 'Root Canal', price: 900.00, category: 'Endodontic' },
      { id: '7', description: 'Tooth Extraction', price: 200.00, category: 'Surgical' },
      { id: '8', description: 'Fluoride Treatment', price: 75.00, category: 'Preventive' }
    ])
  }, [])

  const totalAmount = formData.services.reduce((sum, service) => sum + service.amount, 0)

  const handlePatientChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData(prev => ({ ...prev, patientId: e.target.value }))
  }

  const handleServiceAdd = () => {
    if (!selectedService) return

    const service = services.find(s => s.id === selectedService)
    if (!service) return

    const newService = {
      serviceId: service.id,
      description: service.description,
      quantity: 1,
      unitPrice: service.price,
      amount: service.price
    }

    setFormData(prev => ({
      ...prev,
      services: [...prev.services, newService]
    }))

    setSelectedService('')
  }

  const updateService = (index: number, field: string, value: any) => {
    const updatedServices = [...formData.services]
    
    if (field === 'quantity' || field === 'unitPrice') {
      updatedServices[index] = {
        ...updatedServices[index],
        [field]: Number(value),
        amount: field === 'quantity' 
          ? Number(value) * updatedServices[index].unitPrice
          : updatedServices[index].quantity * Number(value)
      }
    } else {
      updatedServices[index] = { ...updatedServices[index], [field]: value }
    }

    setFormData(prev => ({ ...prev, services: updatedServices }))
  }

  const removeService = (index: number) => {
    setFormData(prev => ({
      ...prev,
      services: prev.services.filter((_, i) => i !== index)
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      // Generate invoice number
      const invoiceNumber = `INV-${new Date().getFullYear()}-${Math.random().toString(36).substr(2, 6).toUpperCase()}`
      
      const invoiceData = {
        ...formData,
        invoiceNumber,
        amount: totalAmount,
        paidAmount: 0
      }

      console.log('Submitting invoice data:', invoiceData)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      router.push('/billing')
    } catch (error) {
      console.error('Error creating invoice:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/billing" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
            ← Back to Billing
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Create New Invoice</h1>
          <p className="text-gray-600 mt-2">Generate a new invoice for patient services</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Patient Selection */}
            <div className="md:col-span-2">
              <label htmlFor="patientId" className="block text-sm font-medium text-gray-700 mb-2">
                Select Patient *
              </label>
              <select
                id="patientId"
                required
                value={formData.patientId}
                onChange={handlePatientChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Choose a patient...</option>
                {patients.map(patient => (
                  <option key={patient.id} value={patient.id}>
                    {patient.firstName} {patient.lastName} - {patient.phone}
                  </option>
                ))}
              </select>
            </div>

            {/* Dates */}
            <div>
              <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-2">
                Invoice Date *
              </label>
              <input
                type="date"
                id="date"
                required
                value={formData.date}
                onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 mb-2">
                Due Date *
              </label>
              <input
                type="date"
                id="dueDate"
                required
                value={formData.dueDate}
                onChange={(e) => setFormData(prev => ({ ...prev, dueDate: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Terms */}
            <div className="md:col-span-2">
              <label htmlFor="terms" className="block text-sm font-medium text-gray-700 mb-2">
                Payment Terms
              </label>
              <select
                id="terms"
                value={formData.terms}
                onChange={(e) => setFormData(prev => ({ ...prev, terms: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Net 15">Net 15</option>
                <option value="Net 30">Net 30</option>
                <option value="Net 60">Net 60</option>
                <option value="Due on Receipt">Due on Receipt</option>
              </select>
            </div>
          </div>

          {/* Services */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Services</h3>
            
            {/* Add Service */}
            <div className="flex gap-4 mb-4">
              <select
                value={selectedService}
                onChange={(e) => setSelectedService(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a service...</option>
                {services.map(service => (
                  <option key={service.id} value={service.id}>
                    {service.description} - {formatCurrency(service.price)}
                  </option>
                ))}
              </select>
              <button
                type="button"
                onClick={handleServiceAdd}
                disabled={!selectedService}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Add Service
              </button>
            </div>

            {/* Services List */}
            {formData.services.length > 0 && (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Description</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Quantity</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Unit Price</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Amount</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {formData.services.map((service, index) => (
                      <tr key={index}>
                        <td className="px-4 py-3">
                          <input
                            type="text"
                            value={service.description}
                            onChange={(e) => updateService(index, 'description', e.target.value)}
                            className="w-full px-2 py-1 border border-gray-300 rounded-md"
                          />
                        </td>
                        <td className="px-4 py-3">
                          <input
                            type="number"
                            min="1"
                            value={service.quantity}
                            onChange={(e) => updateService(index, 'quantity', e.target.value)}
                            className="w-20 px-2 py-1 border border-gray-300 rounded-md"
                          />
                        </td>
                        <td className="px-4 py-3">
                          <input
                            type="number"
                            step="0.01"
                            min="0"
                            value={service.unitPrice}
                            onChange={(e) => updateService(index, 'unitPrice', e.target.value)}
                            className="w-24 px-2 py-1 border border-gray-300 rounded-md"
                          />
                        </td>
                        <td className="px-4 py-3 text-sm font-medium">
                          {formatCurrency(service.amount)}
                        </td>
                        <td className="px-4 py-3">
                          <button
                            type="button"
                            onClick={() => removeService(index)}
                            className="text-red-600 hover:text-red-900"
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot className="bg-gray-50">
                    <tr>
                      <td colSpan={3} className="px-4 py-3 text-right text-sm font-medium text-gray-700">
                        Total Amount:
                      </td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">
                        {formatCurrency(totalAmount)}
                      </td>
                      <td></td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            )}
          </div>

          {/* Notes */}
          <div className="mb-8">
            <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-2">
              Notes
            </label>
            <textarea
              id="notes"
              rows={4}
              value={formData.notes}
              onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Additional notes for the invoice..."
            />
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
            <Link
              href="/billing"
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading || formData.services.length === 0 || !formData.patientId}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating Invoice...' : 'Create Invoice'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}