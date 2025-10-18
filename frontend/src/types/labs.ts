// src/types/labs.ts
export interface LabOrder {
  id: number;
  patientId: number;
  dentistId: number;
  labId: string;
  type: LabOrderType;
  status: LabOrderStatus;
  priority: PriorityLevel;
  specimens: Specimen[];
  tests: LabTest[];
  instructions?: string;
  dueDate: Date;
  completedDate?: Date;
  results?: LabResults;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  dentist?: User;
  lab?: Organization;
}

export interface Specimen {
  type: SpecimenType;
  collectionDate: Date;
  collector: string;
  quantity: string;
  container: string;
  notes?: string;
}

export interface LabTest {
  code: string;
  name: string;
  description?: string;
  parameters: TestParameters;
  expectedResults?: ExpectedResults;
}

export interface LabResults {
  findings: Finding[];
  interpretations: Interpretation[];
  recommendations: Recommendation[];
  attachments: Attachment[];
  signedBy: string;
  signedDate: Date;
}

export interface Finding {
  testCode: string;
  result: string;
  units: string;
  referenceRange: string;
  flag: 'normal' | 'high' | 'low' | 'critical';
}

export interface Interpretation {
  text: string;
  severity: 'normal' | 'mild' | 'moderate' | 'severe';
}

export interface Recommendation {
  action: string;
  priority: PriorityLevel;
  followUp?: Date;
}

export enum LabOrderType {
  BLOOD_TEST = 'blood_test',
  URINE_TEST = 'urine_test',
  IMAGING = 'imaging',
  BIOPSY = 'biopsy',
  CULTURE = 'culture',
  GENETIC = 'genetic'
}

export enum LabOrderStatus {
  REQUESTED = 'requested',
  COLLECTED = 'collected',
  IN_TRANSIT = 'in_transit',
  RECEIVED = 'received',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
}

export enum SpecimenType {
  BLOOD = 'blood',
  URINE = 'urine',
  SALIVA = 'saliva',
  TISSUE = 'tissue',
  SWAB = 'swab'
}