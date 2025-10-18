// frontend/src/features/appointments/AppointmentList.tsx
'use client'

import { useEffect, useState } from "react"
import { fetcher } from "@/services/fetcher"

interface Appointment {
  id: number
  patient: string
  date: string
  time: string
  status: string
}

export default function AppointmentList() {
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadAppointments = async () => {
      try {
        const data = await fetcher("/appointments") // ✅ make sure this API path matches your backend
        setAppointments(data)
      } catch (err) {
        console.error("Failed to load appointments:", err)
      } finally {
        setLoading(false)
      }
    }

    loadAppointments()
  }, [])

  if (loading) return <p>Loading appointments...</p>

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Appointments</h2>
      <ul className="divide-y divide-gray-200">
        {appointments.map((appt) => (
          <li key={appt.id} className="py-4">
            <div className="flex justify-between">
              <span>{appt.patient}</span>
              <span>{appt.date} {appt.time}</span>
              <span className="text-sm text-gray-500">{appt.status}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
