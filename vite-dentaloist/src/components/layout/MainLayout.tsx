// src/components/layout/MainLayout.tsx
// import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Navbar from './Navbar'
import { useUIStore } from '@/app/store'

export default function MainLayout() {
  const sidebarOpen = useUIStore((state) => state.sidebarOpen)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className={sidebarOpen ? 'lg:ml-64' : 'lg:ml-20'}>
        <Navbar />
        
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}