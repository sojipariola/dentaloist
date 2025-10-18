// src/types/custom-forms.ts
export interface CustomForm {
  id: number;
  name: string;
  description?: string;
  type: FormType;
  category: FormCategory;
  version: string;
  fields: FormField[];
  logic: FormLogic[];
  validation: FormValidation;
  styling: FormStyling;
  access: FormAccess;
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

export interface FormStyling {
  theme: FormTheme;
  layout: FormLayout;
  colors: FormColors;
  fonts: FormFonts;
  spacing: FormSpacing;
}

export interface FormAccess {
  roles: string[];
  users: number[];
  groups: string[];
  conditions: AccessCondition[];
}

export interface AccessCondition {
  field: string;
  operator: ConditionOperator;
  value: any;
}

export interface FormColors {
  primary: string;
  secondary: string;
  background: string;
  text: string;
  border: string;
}

export interface FormFonts {
  family: string;
  size: string;
  weight: string;
}

export interface FormSpacing {
  padding: string;
  margin: string;
  gap: string;
}

export enum FormTheme {
  LIGHT = 'light',
  DARK = 'dark',
  AUTO = 'auto'
}

export enum FormLayout {
  SINGLE_COLUMN = 'single_column',
  TWO_COLUMNS = 'two_columns',
  RESPONSIVE = 'responsive'
}