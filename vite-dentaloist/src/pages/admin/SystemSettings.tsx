import React, { useState } from 'react'
import { 
  Save,
  Building,
  Calendar,
  DollarSign,
  Bell,
  Shield,
  Database,
  Mail,
  Clock,
  Users
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock settings data
const initialSettings = {
  practice: {
    name: 'Bright Smile Dental Clinic',
    address: '123 Dental Street',
    city: 'San Francisco',
    state: 'CA',
    zipCode: '94102',
    phone: '(555) 123-4567',
    email: 'info@brightsmiledental.com',
    website: 'www.brightsmiledental.com',
    taxId: '12-3456789'
  },
  scheduling: {
    slotDuration: 30,
    workingHoursStart: '08:00',
    workingHoursEnd: '17:00',
    appointmentBuffer: 15,
    maxAppointmentsPerDay: 20,
    allowOnlineBooking: true,
    bookingLeadTime: 24
  },
  billing: {
    currency: 'USD',
    taxRate: 8.5,
    paymentTerms: 'Due upon receipt',
    lateFeePercentage: 1.5,
    invoicePrefix: 'INV',
    estimatePrefix: 'EST'
  },
  notifications: {
    emailNotifications: true,
    smsNotifications: true,
    appointmentReminders: true,
    paymentReminders: true,
    lowStockAlerts: true,
    systemAlerts: true
  },
  security: {
    sessionTimeout: 60,
    passwordExpiry: 90,
    twoFactorAuth: false,
    loginAttempts: 5,
    ipWhitelist: '',
    auditLogRetention: 365
  }
}

export default function SystemSettings() {
  const [settings, setSettings] = useState(initialSettings)
  const [activeTab, setActiveTab] = useState('practice')
  const [isSaving, setIsSaving] = useState(false)

  const handleSave = async () => {
    setIsSaving(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsSaving(false)
    // In real app, this would save to backend
  }

  const handleInputChange = (section: string, field: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section as keyof typeof prev],
        [field]: value
      }
    }))
  }

  const tabs = [
    { id: 'practice', name: 'Practice Info', icon: Building },
    { id: 'scheduling', name: 'Scheduling', icon: Calendar },
    { id: 'billing', name: 'Billing', icon: DollarSign },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'advanced', name: 'Advanced', icon: Database }
  ]

  const renderPracticeSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input
          label="Practice Name"
          value={settings.practice.name}
          onChange={(e) => handleInputChange('practice', 'name', e.target.value)}
        />
        <Input
          label="Phone Number"
          value={settings.practice.phone}
          onChange={(e) => handleInputChange('practice', 'phone', e.target.value)}
        />
        <Input
          label="Address"
          value={settings.practice.address}
          onChange={(e) => handleInputChange('practice', 'address', e.target.value)}
        />
        <Input
          label="Email"
          type="email"
          value={settings.practice.email}
          onChange={(e) => handleInputChange('practice', 'email', e.target.value)}
        />
        <Input
          label="City"
          value={settings.practice.city}
          onChange={(e) => handleInputChange('practice', 'city', e.target.value)}
        />
        <Input
          label="Website"
          value={settings.practice.website}
          onChange={(e) => handleInputChange('practice', 'website', e.target.value)}
        />
        <Input
          label="State"
          value={settings.practice.state}
          onChange={(e) => handleInputChange('practice', 'state', e.target.value)}
        />
        <Input
          label="Tax ID"
          value={settings.practice.taxId}
          onChange={(e) => handleInputChange('practice', 'taxId', e.target.value)}
        />
        <Input
          label="ZIP Code"
          value={settings.practice.zipCode}
          onChange={(e) => handleInputChange('practice', 'zipCode', e.target.value)}
        />
      </div>
    </div>
  )

  const renderSchedulingSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Appointment Slot Duration (minutes)
          </label>
          <select
            value={settings.scheduling.slotDuration}
            onChange={(e) => handleInputChange('scheduling', 'slotDuration', parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value={15}>15 minutes</option>
            <option value={30}>30 minutes</option>
            <option value={45}>45 minutes</option>
            <option value={60}>60 minutes</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Working Hours Start
          </label>
          <Input
            type="time"
            value={settings.scheduling.workingHoursStart}
            onChange={(e) => handleInputChange('scheduling', 'workingHoursStart', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Working Hours End
          </label>
          <Input
            type="time"
            value={settings.scheduling.workingHoursEnd}
            onChange={(e) => handleInputChange('scheduling', 'workingHoursEnd', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Appointment Buffer (minutes)
          </label>
          <Input
            type="number"
            value={settings.scheduling.appointmentBuffer}
            onChange={(e) => handleInputChange('scheduling', 'appointmentBuffer', parseInt(e.target.value))}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Max Appointments Per Day
          </label>
          <Input
            type="number"
            value={settings.scheduling.maxAppointmentsPerDay}
            onChange={(e) => handleInputChange('scheduling', 'maxAppointmentsPerDay', parseInt(e.target.value))}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Booking Lead Time (hours)
          </label>
          <Input
            type="number"
            value={settings.scheduling.bookingLeadTime}
            onChange={(e) => handleInputChange('scheduling', 'bookingLeadTime', parseInt(e.target.value))}
          />
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <input
          type="checkbox"
          id="allowOnlineBooking"
          checked={settings.scheduling.allowOnlineBooking}
          onChange={(e) => handleInputChange('scheduling', 'allowOnlineBooking', e.target.checked)}
          className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
        />
        <label htmlFor="allowOnlineBooking" className="text-sm font-medium text-gray-700">
          Allow Online Appointment Booking
        </label>
      </div>
    </div>
  )

  const renderBillingSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input
          label="Currency"
          value={settings.billing.currency}
          onChange={(e) => handleInputChange('billing', 'currency', e.target.value)}
        />
        <Input
          label="Tax Rate (%)"
          type="number"
          step="0.1"
          value={settings.billing.taxRate}
          onChange={(e) => handleInputChange('billing', 'taxRate', parseFloat(e.target.value))}
        />
        <Input
          label="Payment Terms"
          value={settings.billing.paymentTerms}
          onChange={(e) => handleInputChange('billing', 'paymentTerms', e.target.value)}
        />
        <Input
          label="Late Fee Percentage (%)"
          type="number"
          step="0.1"
          value={settings.billing.lateFeePercentage}
          onChange={(e) => handleInputChange('billing', 'lateFeePercentage', parseFloat(e.target.value))}
        />
        <Input
          label="Invoice Prefix"
          value={settings.billing.invoicePrefix}
          onChange={(e) => handleInputChange('billing', 'invoicePrefix', e.target.value)}
        />
        <Input
          label="Estimate Prefix"
          value={settings.billing.estimatePrefix}
          onChange={(e) => handleInputChange('billing', 'estimatePrefix', e.target.value)}
        />
      </div>
    </div>
  )

  const renderTabContent = () => {
    switch (activeTab) {
      case 'practice':
        return renderPracticeSettings()
      case 'scheduling':
        return renderSchedulingSettings()
      case 'billing':
        return renderBillingSettings()
      case 'notifications':
        return (
          <div className="space-y-4">
            {Object.entries(settings.notifications).map(([key, value]) => (
              <div key={key} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id={key}
                  checked={value as boolean}
                  onChange={(e) => handleInputChange('notifications', key, e.target.checked)}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor={key} className="text-sm font-medium text-gray-700 capitalize">
                  {key.replace(/([A-Z])/g, ' $1').toLowerCase()}
                </label>
              </div>
            ))}
          </div>
        )
      case 'security':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="Session Timeout (minutes)"
                type="number"
                value={settings.security.sessionTimeout}
                onChange={(e) => handleInputChange('security', 'sessionTimeout', parseInt(e.target.value))}
              />
              <Input
                label="Password Expiry (days)"
                type="number"
                value={settings.security.passwordExpiry}
                onChange={(e) => handleInputChange('security', 'passwordExpiry', parseInt(e.target.value))}
              />
              <Input
                label="Max Login Attempts"
                type="number"
                value={settings.security.loginAttempts}
                onChange={(e) => handleInputChange('security', 'loginAttempts', parseInt(e.target.value))}
              />
              <Input
                label="Audit Log Retention (days)"
                type="number"
                value={settings.security.auditLogRetention}
                onChange={(e) => handleInputChange('security', 'auditLogRetention', parseInt(e.target.value))}
              />
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="twoFactorAuth"
                checked={settings.security.twoFactorAuth}
                onChange={(e) => handleInputChange('security', 'twoFactorAuth', e.target.checked)}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="twoFactorAuth" className="text-sm font-medium text-gray-700">
                Enable Two-Factor Authentication
              </label>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                IP Whitelist (comma-separated)
              </label>
              <Input
                value={settings.security.ipWhitelist}
                onChange={(e) => handleInputChange('security', 'ipWhitelist', e.target.value)}
                placeholder="192.168.1.1, 10.0.0.1"
              />
            </div>
          </div>
        )
      default:
        return <div>Settings for this section are under development.</div>
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">System Settings</h1>
          <p className="text-gray-600 mt-2">Configure your practice management system</p>
        </div>
        <Button onClick={handleSave} loading={isSaving}>
          <Save className="h-4 w-4 mr-2" />
          Save Changes
        </Button>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar Navigation */}
        <div className="lg:w-64">
          <Card className="p-4">
            <nav className="space-y-1">
              {tabs.map((tab) => {
                const IconComponent = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary-100 text-primary-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    <IconComponent className="h-4 w-4" />
                    <span>{tab.name}</span>
                  </button>
                )
              })}
            </nav>
          </Card>
        </div>

        {/* Settings Content */}
        <div className="flex-1">
          <Card className="p-6">
            {renderTabContent()}
          </Card>
        </div>
      </div>
    </div>
  )
}