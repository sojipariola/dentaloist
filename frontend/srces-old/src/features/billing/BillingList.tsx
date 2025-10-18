// frontend/src/features/billing/BillingList.tsx
'use client'

import { useEffect, useState } from "react"
import { fetcher } from "../../services/api"

interface Invoice {
  id: number
  patient: string
  amount: number
  date: string
  status: string
}

export default function BillingList() {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadInvoices = async () => {
      try {
        const data = await fetcher("/billing") // ✅ adjust API path to match your backend
        setInvoices(data)
      } catch (err) {
        console.error("Failed to load invoices:", err)
      } finally {
        setLoading(false)
      }
    }

    loadInvoices()
  }, [])

  if (loading) return <p>Loading invoices...</p>

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Billing</h2>
      <ul className="divide-y divide-gray-200">
        {invoices.map((invoice) => (
          <li key={invoice.id} className="py-4">
            <div className="flex justify-between">
              <span>{invoice.patient}</span>
              <span>${invoice.amount}</span>
              <span>{invoice.date}</span>
              <span className="text-sm text-gray-500">{invoice.status}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
