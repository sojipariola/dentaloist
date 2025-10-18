// src/types/inventory.ts
export interface InventoryItem {
  id: number;
  name: string;
  description?: string;
  category: InventoryCategory;
  sku: string;
  barcode?: string;
  unit: InventoryUnit;
  quantity: number;
  minQuantity: number;
  maxQuantity: number;
  cost: number;
  price: number;
  supplierId?: string;
  location?: string;
  expiryDate?: Date;
  lotNumber?: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  supplier?: Organization;
}

export interface InventoryTransaction {
  id: number;
  itemId: number;
  type: TransactionType;
  quantity: number;
  unitCost: number;
  totalCost: number;
  referenceType?: ReferenceType;
  referenceId?: number;
  notes?: string;
  performedBy: number;
  createdAt: Date;
  
  // Relations
  item?: InventoryItem;
  performedByUser?: User;
}

export interface Supplier {
  id: string;
  name: string;
  contact: ContactInfo;
  products: string[];
  paymentTerms: string;
  rating: number;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface ContactInfo {
  email: string;
  phone: string;
  address: Address;
}

export enum InventoryCategory {
  MEDICAL_SUPPLIES = 'medical_supplies',
  DENTAL_MATERIALS = 'dental_materials',
  MEDICATION = 'medication',
  EQUIPMENT = 'equipment',
  OFFICE_SUPPLIES = 'office_supplies'
}

export enum InventoryUnit {
  PIECE = 'piece',
  PACK = 'pack',
  BOX = 'box',
  BOTTLE = 'bottle',
  ROLL = 'roll',
  METER = 'meter'
}

export enum TransactionType {
  PURCHASE = 'purchase',
  SALE = 'sale',
  ADJUSTMENT = 'adjustment',
  TRANSFER = 'transfer',
  RETURN = 'return'
}

export enum ReferenceType {
  APPOINTMENT = 'appointment',
  ORDER = 'order',
  ADJUSTMENT = 'adjustment'
}