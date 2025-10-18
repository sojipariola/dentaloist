import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Button, Card } from '@/components/ui'

export default function Component() {
  const isEdit = location.pathname.includes('/edit')
  
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
          {isEdit ? 'Edit' : 'Create New'} {(() => {
            const name = location.pathname.split('/').slice(-2, -1)[0]
            return name.split(/(?=[A-Z])/).join(' ')
          })()}
        </h1>
      </div>

      <Card className="p-8">
        <div className="text-center text-gray-500">
          <p className="text-lg mb-2">Form under development</p>
          <p className="text-sm">This form will be implemented in the next stage</p>
        </div>
      </Card>
    </div>
  )
}
