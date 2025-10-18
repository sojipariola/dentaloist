import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { appointmentsService, type Appointment, type AppointmentFilters } from '@/api/services'

export const useAppointments = (filters: AppointmentFilters = {}) => {
  return useQuery({
    queryKey: ['appointments', filters],
    queryFn: () => appointmentsService.getAppointments(filters),
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

export const useAppointment = (id: number) => {
  return useQuery({
    queryKey: ['appointment', id],
    queryFn: () => appointmentsService.getAppointment(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export const useCreateAppointment = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: appointmentsService.createAppointment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['appointments'] })
    },
  })
}

export const useUpdateAppointment = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Appointment> }) =>
      appointmentsService.updateAppointment(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['appointments'] })
      queryClient.invalidateQueries({ queryKey: ['appointment', variables.id] })
    },
  })
}

export const useDeleteAppointment = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: appointmentsService.deleteAppointment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['appointments'] })
    },
  })
}