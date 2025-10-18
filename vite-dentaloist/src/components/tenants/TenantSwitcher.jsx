// TenantSwitcher.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const TenantSwitcher = () => {
  const { user, tenants, switchTenant } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  
  if (!user?.is_super_admin || tenants.length <= 1) {
    return null;
  }
  
  const currentTenant = tenants.find(t => t.is_current) || tenants[0];
  
  return (
    <div className="tenant-switcher">
      <button 
        className="tenant-switcher-toggle"
        onClick={() => setIsOpen(!isOpen)}
      >
        🏢 {currentTenant?.name} ▼
      </button>
      
      {isOpen && (
        <div className="tenant-dropdown">
          <div className="tenant-dropdown-header">
            Switch Organization
          </div>
          {tenants.map(tenant => (
            <button
              key={tenant.id}
              className={`tenant-option ${tenant.is_current ? 'current' : ''}`}
              onClick={() => {
                switchTenant(tenant.id);
                setIsOpen(false);
              }}
            >
              <span className="tenant-name">{tenant.name}</span>
              {tenant.is_current && <span className="current-badge">Current</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default TenantSwitcher;