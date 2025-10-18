import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Package, 
  Plus, 
  Search,
  Filter,
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  MoreHorizontal
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data
const mockInventoryItems = [
  {
    id: 1,
    name: 'Dental Anesthetic Cartridges',
    sku: 'ANES-001',
    category: 'Anesthetics',
    current_stock: 45,
    min_stock_level: 20,
    max_stock_level: 100,
    cost_price: 8.50,
    selling_price: 15.00,
    supplier: 'Dental Supplies Inc.',
    last_ordered: '2024-01-10T00:00:00Z',
    status: 'in_stock'
  },
  {
    id: 2,
    name: 'Disposable Gloves (Medium)',
    sku: 'GLOV-002',
    category: 'Disposables',
    current_stock: 15,
    min_stock_level: 25,
    max_stock_level: 200,
    cost_price: 0.25,
    selling_price: 0.75,
    supplier: 'MediSupply Co.',
    last_ordered: '2024-01-05T00:00:00Z',
    status: 'low_stock'
  },
  {
    id: 3,
    name: 'Composite Filling Material',
    sku: 'FILL-003',
    category: 'Restoratives',
    current_stock: 0,
    min_stock_level: 10,
    max_stock_level: 50,
    cost_price: 45.00,
    selling_price: 85.00,
    supplier: 'Dental Materials Ltd.',
    last_ordered: '2024-01-15T00:00:00Z',
    status: 'out_of_stock'
  }
]

export default function InventoryItems() {
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredItems = mockInventoryItems.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.sku.toLowerCase().includes(searchTerm.toLowerCase())
  ).filter(item => 
    (categoryFilter === 'all' || item.category === categoryFilter) &&
    (statusFilter === 'all' || item.status === statusFilter)
  )

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount)
  }

  const getStatusColor = (status: string) => {
    const colors = {
      in_stock: 'bg-green-100 text-green-800',
      low_stock: 'bg-yellow-100 text-yellow-800',
      out_of_stock: 'bg-red-100 text-red-800',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  const getStatusText = (status: string) => {
    const texts = {
      in_stock: 'In Stock',
      low_stock: 'Low Stock',
      out_of_stock: 'Out of Stock',
    }
    return texts[status as keyof typeof texts] || status
  }

  const getStockPercentage = (current: number, max: number) => {
    return (current / max) * 100
  }

  const getStockTrend = (current: number, min: number) => {
    if (current <= min) return 'critical'
    if (current <= min * 1.5) return 'warning'
    return 'good'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Inventory</h1>
          <p className="text-gray-600 mt-2">Manage dental supplies and equipment</p>
        </div>
        <Button asChild>
          <Link to="/inventory/items/new">
            <Plus className="h-4 w-4 mr-2" />
            Add Item
          </Link>
        </Button>
      </div>

      {/* Inventory Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Items</p>
              <p className="text-2xl font-bold text-gray-900">156</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <Package className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Low Stock</p>
              <p className="text-2xl font-bold text-gray-900">12</p>
            </div>
            <div className="p-3 bg-yellow-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-yellow-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Out of Stock</p>
              <p className="text-2xl font-bold text-gray-900">3</p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <Package className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Value</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatCurrency(12540.75)}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search inventory by name or SKU..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              icon={Search}
            />
          </div>
          <div className="flex flex-wrap gap-2">
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Categories</option>
              <option value="Anesthetics">Anesthetics</option>
              <option value="Disposables">Disposables</option>
              <option value="Restoratives">Restoratives</option>
              <option value="Equipment">Equipment</option>
            </select>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="in_stock">In Stock</option>
              <option value="low_stock">Low Stock</option>
              <option value="out_of_stock">Out of Stock</option>
            </select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Inventory Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredItems.map((item) => {
          const stockTrend = getStockTrend(item.current_stock, item.min_stock_level)
          return (
            <Card key={item.id} className="p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="font-semibold text-gray-900">{item.name}</h3>
                  <p className="text-sm text-gray-600">{item.sku}</p>
                </div>
                <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(item.status)}`}>
                  {getStatusText(item.status)}
                </span>
              </div>

              <div className="space-y-3 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Category</span>
                  <span className="font-medium">{item.category}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Supplier</span>
                  <span className="font-medium">{item.supplier}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Cost/Price</span>
                  <span className="font-medium">
                    {formatCurrency(item.cost_price)} / {formatCurrency(item.selling_price)}
                  </span>
                </div>
              </div>

              {/* Stock Level Bar */}
              <div className="mb-2">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Stock Level</span>
                  <span className="font-medium">
                    {item.current_stock} / {item.max_stock_level}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${
                      stockTrend === 'critical' ? 'bg-red-500' :
                      stockTrend === 'warning' ? 'bg-yellow-500' :
                      'bg-green-500'
                    }`}
                    style={{ 
                      width: `${getStockPercentage(item.current_stock, item.max_stock_level)}%` 
                    }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Min: {item.min_stock_level}</span>
                  <span>Max: {item.max_stock_level}</span>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-600">
                <span>Last ordered: {formatDate(item.last_ordered)}</span>
                {stockTrend === 'critical' && (
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                )}
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm" className="flex-1">
                    Order
                  </Button>
                  <Button variant="outline" size="sm">
                    Edit
                  </Button>
                </div>
              </div>
            </Card>
          )
        })}
      </div>

      {filteredItems.length === 0 && (
        <Card className="p-8 text-center">
          <Package className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No inventory items found</h3>
          <p className="text-gray-600 mb-4">
            {searchTerm || categoryFilter !== 'all' || statusFilter !== 'all'
              ? 'Try adjusting your search or filters'
              : 'Get started by adding your first inventory item'
            }
          </p>
          {!(searchTerm || categoryFilter !== 'all' || statusFilter !== 'all') && (
            <Button asChild>
              <Link to="/inventory/items/new">
                <Plus className="h-4 w-4 mr-2" />
                Add Inventory Item
              </Link>
            </Button>
          )}
        </Card>
      )}
    </div>
  )
}