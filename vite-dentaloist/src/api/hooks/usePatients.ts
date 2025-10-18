import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { patientsService, type Patient, type PatientFilters } from '@/api/services'

export const usePatients = (filters: PatientFilters = {}) => {
  return useQuery({
    queryKey: ['patients', filters],
    queryFn: () => patientsService.getPatients(filters),
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

export const usePatient = (id: number) => {
  return useQuery({
    queryKey: ['patient', id],
    queryFn: () => patientsService.getPatient(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export const useCreatePatient = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: patientsService.createPatient,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['patients'] })
    },
  })
}

export const useUpdatePatient = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Patient> }) =>
      patientsService.updatePatient(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['patients'] })
      queryClient.invalidateQueries({ queryKey: ['patient', variables.id] })
    },
  })
}

export const useDeletePatient = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: patientsService.deletePatient,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['patients'] })
    },
  })
}

export const usePatientStats = () => {
  return useQuery({
    queryKey: ['patient-stats'],
    queryFn: patientsService.getPatientStats,
    staleTime: 10 * 60 * 1000, // 10 minutes
  })
}