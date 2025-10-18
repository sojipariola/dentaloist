// src/components/OrganizationInfo.tsx
import { useEffect, useState } from "react";
import { apiClient } from "../../services/api";
import { useAuth } from "../../contexts/AuthContext";
import { Organization } from "@/types";

interface OrganizationInfoProps {
  organizationId?: number;
}

export default function OrganizationInfo({ organizationId }: OrganizationInfoProps) {
  const [org, setOrg] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchOrganization = async () => {
      try {
        setLoading(true);
        setError(null);
        
        let response;
        
        if (organizationId) {
          // Fetch specific organization
          response = await apiClient.getOrganization(organizationId);
        } else if (user?.organization_id) {
          // Fetch user's organization
          response = await apiClient.getOrganization(user.organization_id);
        } else {
          // Fetch current organization (for logged-in user)
          response = await apiClient.getCurrentOrganization();
        }

        if (response.data && response.data.organization) {
          setOrg(response.data.organization);
        } else {
          throw new Error('No organization data received');
        }
      } catch (err: any) {
        console.error("Failed to fetch organization:", err);
        setError(err.error || err.message || "Failed to load organization information");
      } finally {
        setLoading(false);
      }
    };

    fetchOrganization();
  }, [user?.organization_id, organizationId]);

  if (loading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-1"></div>
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-red-800 font-semibold">Error</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!org) {
    return (
      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-yellow-800">No organization information available</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-3 text-gray-800">{org.name}</h2>
      <div className="space-y-2 text-sm text-gray-600">
        <p>
          <span className="font-semibold">Type:</span> {org.type}
        </p>
        <p>
          <span className="font-semibold">Subscription Plan:</span>{" "}
          <span className="capitalize">{org.subscription_plan?.replace("_", " ") || 'Not specified'}</span>
        </p>
        {org.max_staff && (
          <p>
            <span className="font-semibold">Max Staff:</span> {org.max_staff}
          </p>
        )}
        {org.max_patients && (
          <p>
            <span className="font-semibold">Max Patients:</span> {org.max_patients}
          </p>
        )}
        <p>
          <span className="font-semibold">Status:</span>{" "}
          <span
            className={`px-2 py-1 rounded text-xs ${
              org.is_active
                ? "bg-green-100 text-green-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {org.is_active ? "Active" : "Inactive"}
          </span>
        </p>
        {org.created_at && (
          <p>
            <span className="font-semibold">Created:</span>{" "}
            {new Date(org.created_at).toLocaleDateString()}
          </p>
        )}
      </div>
    </div>
  );
}