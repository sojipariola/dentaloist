import React from 'react'
import { Card } from '@/components/ui'

export default function Component() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        {(() => {
          const name = location.pathname.split('/').pop() || 'Page'
          return name.charAt(0).toUpperCase() + name.slice(1)
        })()}
      </h1>
      <Card className="p-8">
        <div className="text-center text-gray-500">
          <p className="text-lg">This page is under development</p>
          <p className="text-sm mt-2">Coming soon in Stage 4</p>
        </div>
      </Card>
    </div>
  )
}
