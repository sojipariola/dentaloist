import api from './api'

export async function getPatients() {
  const res = await api.get('/patients')
  return res.data
}
