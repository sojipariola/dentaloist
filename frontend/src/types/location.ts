// src/types/location.ts
export interface Location {
  id: number;
  name: string;
  type: LocationType;
  address: Address;
  contact: ContactInfo;
  timezone: string;
  businessHours: BusinessHours;
  facilities: Facility[];
  equipment: Equipment[];
  capacity: Capacity;
  status: LocationStatus;
  settings: LocationSettings;
  createdAt: Date;
  updatedAt: Date;
}

export interface Facility {
  type: FacilityType;
  name: string;
  description?: string;
  equipment: string[];
  capacity: number;
  available: boolean;
}

export interface Equipment {
  type: EquipmentType;
  name: string;
  model: string;
  serialNumber: string;
  status: EquipmentStatus;
  lastMaintenance?: Date;
  nextMaintenance?: Date;
  warranty: WarrantyInfo;
}

export interface Capacity {
  totalRooms: number;
  availableRooms: number;
  maxPatients: number;
  currentPatients: number;
  waitingArea: number;
}

export interface LocationSettings {
  appointmentDuration: number;
  bufferTime: number;
  maxOverbook: number;
  autoConfirm: boolean;
  reminderSettings: ReminderSettings;
}

export interface WarrantyInfo {
  start: Date;
  end: Date;
  provider: string;
  contact: string;
}

export enum LocationType {
  CLINIC = 'clinic',
  HOSPITAL = 'hospital',
  LAB = 'lab',
  IMAGING_CENTER = 'imaging_center',
  SURGICAL_CENTER = 'surgical_center',
  URGENT_CARE = 'urgent_care'
}

export enum LocationStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  MAINTENANCE = 'maintenance',
  CLOSED = 'closed'
}

export enum FacilityType {
  EXAM_ROOM = 'exam_room',
  OPERATING_ROOM = 'operating_room',
  LAB_ROOM = 'lab_room',
  IMAGING_ROOM = 'imaging_room',
  RECOVERY_ROOM = 'recovery_room',
  WAITING_ROOM = 'waiting_room'
}

export enum EquipmentType {
  DIAGNOSTIC = 'diagnostic',
  SURGICAL = 'surgical',
  LAB = 'lab',
  IMAGING = 'imaging',
  MONITORING = 'monitoring',
  SUPPORT = 'support'
}

export enum EquipmentStatus {
  OPERATIONAL = 'operational',
  MAINTENANCE = 'maintenance',
  OUT_OF_SERVICE = 'out_of_service',
  RETIRED = 'retired'
}