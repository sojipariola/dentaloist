// src/types/forms.ts
export interface Form {
  id: number;
  name: string;
  description?: string;
  type: FormType;
  category: FormCategory;
  version: string;
  fields: FormField[];
  logic: FormLogic[];
  validation: FormValidation;
  isActive: boolean;
  isTemplate: boolean;
  organizationId: string;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  organization?: Organization;
  createdByUser?: User;
  submissions?: FormSubmission[];
}

export interface FormField {
  id: string;
  type: FieldType;
  label: string;
  description?: string;
  required: boolean;
  defaultValue?: any;
  options?: FieldOption[];
  validation?: FieldValidation;
  position: number;
  conditions?: FieldCondition[];
}

export interface FormLogic {
  conditions: LogicCondition[];
  actions: LogicAction[];
}

export interface FormSubmission {
  id: number;
  formId: number;
  patientId?: number;
  submittedBy: number;
  data: Record<string, any>;
  status: SubmissionStatus;
  reviewedBy?: number;
  reviewedAt?: Date;
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  form?: Form;
  patient?: Patient;
  submittedByUser?: User;
  reviewedByUser?: User;
}

export interface FieldOption {
  value: string;
  label: string;
}

export interface FieldValidation {
  min?: number;
  max?: number;
  pattern?: string;
  minLength?: number;
  maxLength?: number;
}

export interface FieldCondition {
  fieldId: string;
  operator: ConditionOperator;
  value: any;
}

export interface LogicCondition {
  fieldId: string;
  operator: ConditionOperator;
  value: any;
}

export interface LogicAction {
  type: ActionType;
  target: string;
  value: any;
}

export enum FormType {
  PATIENT_INTAKE = 'patient_intake',
  MEDICAL_HISTORY = 'medical_history',
  CONSENT = 'consent',
  SURVEY = 'survey',
  ASSESSMENT = 'assessment',
  FEEDBACK = 'feedback'
}

export enum FormCategory {
  CLINICAL = 'clinical',
  ADMINISTRATIVE = 'administrative',
  RESEARCH = 'research',
  QUALITY = 'quality'
}

export enum FieldType {
  TEXT = 'text',
  TEXTAREA = 'textarea',
  NUMBER = 'number',
  EMAIL = 'email',
  PHONE = 'phone',
  DATE = 'date',
  DATETIME = 'datetime',
  SELECT = 'select',
  RADIO = 'radio',
  CHECKBOX = 'checkbox',
  FILE = 'file',
  SIGNATURE = 'signature'
}

export enum ConditionOperator {
  EQUALS = 'equals',
  NOT_EQUALS = 'not_equals',
  CONTAINS = 'contains',
  GREATER_THAN = 'greater_than',
  LESS_THAN = 'less_than',
  IS_EMPTY = 'is_empty',
  IS_NOT_EMPTY = 'is_not_empty'
}

export enum ActionType {
  SHOW = 'show',
  HIDE = 'hide',
  ENABLE = 'enable',
  DISABLE = 'disable',
  SET_VALUE = 'set_value',
  REQUIRED = 'required',
  NOT_REQUIRED = 'not_required'
}

export enum SubmissionStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  REVIEWED = 'reviewed',
  APPROVED = 'approved',
  REJECTED = 'rejected'
}