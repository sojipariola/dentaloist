import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Button, Card } from '@/components/ui'

export default function Component() {
  const isEdit = location.pathname.includes('/edit')
  const isNew = location.pathname.includes('/new')
  
  const getPageTitle = () => {
    if (isNew) return 'Create New'
    if (isEdit) return 'Edit'
    return 'System Statistics' // Default for stats page
  }

  const getEntityName = () => {
    const path = location.pathname
    if (path.includes('/users')) return 'User'
    if (path.includes('/roles')) return 'Role'
    if (path.includes('/database')) return 'Database Management'
    return 'System Statistics'
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="ghost" asChild>
          <Link to="..">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Link>
        </Button>
        <h1 className="text-3xl font-bold text-gray-900">
          {getPageTitle()} {getEntityName()}
        </h1>
      </div>

      <Card className="p-8">
        <div className="text-center text-gray-500">
          <p className="text-lg mb-2">
            {isNew || isEdit ? 'Form under development' : 'Page under development'}
          </p>
          <p className="text-sm">
            {isNew || isEdit 
              ? 'This form will be implemented in the next stage'
              : 'This page will be implemented in the next stage'
            }
          </p>
        </div>
      </Card>
    </div>
  )
}
