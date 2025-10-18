// src/types/roles.ts
export interface Role {
  id: number;
  name: string;
  description?: string;
  permissions: Permission[];
  organizationId: string;
  isDefault: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  organization?: Organization;
  users?: User[];
}

export interface RoleCreate {
  name: string;
  description?: string;
  permissions: Permission[];
  organizationId: string;
  isDefault?: boolean;
}

export interface RoleUpdate {
  name?: string;
  description?: string;
  permissions?: Permission[];
  isDefault?: boolean;
}

export enum Permission {
  CREATE_PATIENT = 'create_patient',
  VIEW_PATIENT = 'view_patient',
  EDIT_PATIENT = 'edit_patient',
  DELETE_PATIENT = 'delete_patient',
  CREATE_APPOINTMENT = 'create_appointment',
  VIEW_APPOINTMENT = 'view_appointment',
  EDIT_APPOINTMENT = 'edit_appointment',
  DELETE_APPOINTMENT = 'delete_appointment',
  DIAGNOSE = 'diagnose',
  DESIGN_RESTORATION = 'design_restoration',
  UPLOAD_IMAGES = 'upload_images',
  VIEW_TREATMENT = 'view_treatment',
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
  VIEW_ORGANIZATION = 'view_organization',
  EDIT_ORGANIZATION = 'edit_organization',
  MANAGE_BILLING = 'manage_billing',
  VIEW_BILLING = 'view_billing',
  VIEW_ANALYTICS = 'view_analytics',
  EXPORT_DATA = 'export_data',
  ACCESS_AI_ADVICE = 'access_ai_advice'
}