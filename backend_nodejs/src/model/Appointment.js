const mongoose = require('mongoose');

const appointmentSchema = new mongoose.Schema({
  patient: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  dentist: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  date: { type: Date, required: true },
  startTime: { type: String, required: true },
  endTime: { type: String, required: true },
  duration: { type: Number, required: true }, // in minutes
  type: { 
    type: String, 
    enum: ['checkup', 'cleaning', 'filling', 'extraction', 'root_canal', 'crown', 'other'],
    required: true 
  },
  status: { 
    type: String, 
    enum: ['scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show'],
    default: 'scheduled' 
  },
  reason: String,
  notes: String,
  treatmentPlan: { type: mongoose.Schema.Types.ObjectId, ref: 'TreatmentPlan' },
  room: String,
  priority: { type: String, enum: ['low', 'medium', 'high'], default: 'medium' }
}, { timestamps: true });

module.exports = mongoose.model('Appointment', appointmentSchema);