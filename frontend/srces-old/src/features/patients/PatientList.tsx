// frontend/src/features/patients/PatientList.tsx
'use client'

import { useEffect, useState } from "react"
import { Patient } from "../../types/patient"
import { getPatients } from "../../services/patientService"

export default function PatientList() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadPatients = async () => {
      try {
        const data = await getPatients()
        setPatients(data)
      } catch (err) {
        console.error("Failed to load patients:", err)
      } finally {
        setLoading(false)
      }
    }

    loadPatients()
  }, [])

  if (loading) return <p>Loading patients...</p>

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Patients</h2>
      <ul className="divide-y divide-gray-200">
        {patients.map((patient) => (
          <li key={patient.id} className="py-4">
            <div className="flex justify-between">
              <span>{patient.first_name} {patient.last_name}</span>
              <span>{patient.email}</span>
              <span className="text-sm text-gray-500">{patient.phone}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
