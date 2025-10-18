
import PatientList from "../../features/patients/PatientList";
import AppointmentList from "../../features/appointments/AppointmentList";
import BillingList from "../../features/billing/BillingList";

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <PatientList />
      <AppointmentList />
      <BillingList />
    </div>
  );
}
