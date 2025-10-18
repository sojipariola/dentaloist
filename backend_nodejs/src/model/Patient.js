const mongoose = require('mongoose');

const patientSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  medicalHistory: [{
    condition: String,
    diagnosisDate: Date,
    treatment: String,
    notes: String
  }],
  allergies: [String],
  medications: [{
    name: String,
    dosage: String,
    frequency: String,
    prescribedBy: String
  }],
  insurance: {
    provider: String,
    policyNumber: String,
    groupNumber: String,
    effectiveDate: Date,
    expirationDate: Date
  },
  primaryDentist: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  emergencyContact: {
    name: String,
    relationship: String,
    phone: String
  }
}, { timestamps: true });

module.exports = mongoose.model('Patient', patientSchema);