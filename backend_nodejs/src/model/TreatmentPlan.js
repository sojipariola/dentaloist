const mongoose = require('mongoose');

const treatmentPlanSchema = new mongoose.Schema({
  patient: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  dentist: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  diagnosis: String,
  procedures: [{
    procedure: String,
    toothNumber: String,
    surface: String,
    cost: Number,
    status: { type: String, enum: ['pending', 'in_progress', 'completed'], default: 'pending' },
    scheduledDate: Date,
    completedDate: Date,
    notes: String
  }],
  totalCost: Number,
  status: { type: String, enum: ['active', 'completed', 'cancelled'], default: 'active' },
  startDate: Date,
  expectedEndDate: Date,
  notes: String
}, { timestamps: true });

module.exports = mongoose.model('TreatmentPlan', TreatmentPlan);