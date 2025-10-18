'use client';

import { useEffect, useState } from 'react';
import { patientsApi, Patient } from '@/lib/api/patients';

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const data = await patientsApi.getAll();
        setPatients(data);
      } catch (err) {
        console.error('Failed to load patients', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPatients();
  }, []);

  if (loading) return <p>Loading patients...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold">Patients</h1>
      <ul className="mt-4 space-y-2">
        {patients.map((p) => (
          <li key={p.id} className="border p-2 rounded">
            {p.first_name} {p.last_name} ({p.email || 'No email'})
          </li>
        ))}
      </ul>
    </div>
  );
}
