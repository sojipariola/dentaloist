// components/dashboard/RecentAppointments.tsx
import { motion } from 'framer-motion';
import { Calendar, Clock, User, MapPin } from 'lucide-react';

const appointments = [
  {
    id: 1,
    patient: 'Sarah Johnson',
    time: '9:00 AM',
    duration: '30 min',
    type: 'Cleaning',
    status: 'confirmed',
    dentist: 'Dr. Smith',
  },
  {
    id: 2,
    patient: 'Mike Wilson',
    time: '10:30 AM',
    duration: '45 min',
    type: 'Filling',
    status: 'in-progress',
    dentist: 'Dr. Johnson',
  },
  {
    id: 3,
    patient: 'Emily Davis',
    time: '1:00 PM',
    duration: '1 hour',
    type: 'Root Canal',
    status: 'scheduled',
    dentist: 'Dr. Brown',
  },
  {
    id: 4,
    patient: 'John Miller',
    time: '3:30 PM',
    duration: '30 min',
    type: 'Checkup',
    status: 'scheduled',
    dentist: 'Dr. Wilson',
  },
];

const statusColors = {
  scheduled: 'bg-blue-100 text-blue-800',
  confirmed: 'bg-green-100 text-green-800',
  'in-progress': 'bg-amber-100 text-amber-800',
  completed: 'bg-gray-100 text-gray-800',
  cancelled: 'bg-red-100 text-red-800',
};

export function RecentAppointments() {
  return (
    <motion.div
      className="bg-white rounded-xl p-6 shadow-sm"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Today's Appointments</h3>
        <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
          View All
        </button>
      </div>

      <div className="space-y-4">
        {appointments.map((appointment, index) => (
          <motion.div
            key={appointment.id}
            className="flex items-center justify-between p-4 border rounded-lg hover:shadow-md transition-shadow"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h4 className="font-medium text-gray-900">{appointment.patient}</h4>
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <span className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    {appointment.time}
                  </span>
                  <span>{appointment.duration}</span>
                  <span className="flex items-center">
                    <User className="w-4 h-4 mr-1" />
                    {appointment.dentist}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[appointment.status as keyof typeof statusColors]}`}>
                {appointment.status}
              </span>
              <div className="text-right">
                <p className="font-medium text-gray-900">{appointment.type}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}