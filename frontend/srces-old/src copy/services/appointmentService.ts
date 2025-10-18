import api from './api'

export async function getAppointments() {
  const res = await api.get('/appointments')
  return res.data
}
