import { create } from 'zustand'

interface UIState {
  sidebarOpen: boolean
  currentTheme: 'light' | 'dark'
  notifications: any[]
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  setTheme: (theme: 'light' | 'dark') => void
  addNotification: (notification: any) => void
  removeNotification: (id: string) => void
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: false,
  currentTheme: 'light',
  notifications: [],
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setTheme: (theme) => set({ currentTheme: theme }),
  addNotification: (notification) => 
    set((state) => ({ 
      notifications: [...state.notifications, notification] 
    })),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
}))