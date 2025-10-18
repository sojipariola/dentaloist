const express = require('express');
const Appointment = require('../models/Appointment');
const auth = require('../middleware/auth');

const router = express.Router();

// Get all appointments
router.get('/', auth, async (req, res) => {
  try {
    const { date, dentist, status } = req.query;
    let filter = {};
    
    if (date) filter.date = new Date(date);
    if (dentist) filter.dentist = dentist;
    if (status) filter.status = status;

    const appointments = await Appointment.find(filter)
      .populate('patient', 'firstName lastName email')
      .populate('dentist', 'firstName lastName specialization');
    
    res.json(appointments);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Create appointment
router.post('/', auth, async (req, res) => {
  try {
    const appointment = new Appointment(req.body);
    await appointment.save();
    await appointment.populate(['patient', 'dentist']);
    res.status(201).json(appointment);
  } catch (error) {
    res.status(400).json({ message: 'Error creating appointment', error: error.message });
  }
});

// Update appointment
router.put('/:id', auth, async (req, res) => {
  try {
    const appointment = await Appointment.findByIdAndUpdate(req.params.id, req.body, { new: true })
      .populate('patient', 'firstName lastName email')
      .populate('dentist', 'firstName lastName specialization');
    
    res.json(appointment);
  } catch (error) {
    res.status(400).json({ message: 'Error updating appointment', error: error.message });
  }
});

module.exports = router;