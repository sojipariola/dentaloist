// src/types/supply-chain.ts
export interface SupplyOrder {
  id: number;
  orderNumber: string;
  supplierId: string;
  items: OrderItem[];
  status: OrderStatus;
  priority: OrderPriority;
  totalCost: number;
  shipping: ShippingInfo;
  expectedDelivery: Date;
  actualDelivery?: Date;
  receivedBy?: number;
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  supplier?: Organization;
  receivedByUser?: User;
}

export interface OrderItem {
  itemId: number;
  quantity: number;
  unitCost: number;
  totalCost: number;
  receivedQuantity: number;
  status: ItemStatus;
  item?: InventoryItem;
}

export interface ShippingInfo {
  carrier: string;
  trackingNumber: string;
  cost: number;
  address: Address;
  contact: ContactInfo;
}

export interface InventoryAlert {
  id: number;
  itemId: number;
  type: AlertType;
  severity: AlertSeverity;
  message: string;
  threshold: number;
  currentValue: number;
  isResolved: boolean;
  resolvedAt?: Date;
  resolvedBy?: number;
  createdAt: Date;
  
  // Relations
  item?: InventoryItem;
  resolvedByUser?: User;
}

export interface SupplierPerformance {
  supplierId: string;
  rating: number;
  deliveryTime: number;
  qualityScore: number;
  complianceScore: number;
  totalOrders: number;
  completedOrders: number;
  issues: PerformanceIssue[];
  supplier?: Organization;
}

export enum OrderStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  CONFIRMED = 'confirmed',
  SHIPPED = 'shipped',
  DELIVERED = 'delivered',
  CANCELLED = 'cancelled'
}

export enum OrderPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

export enum ItemStatus {
  PENDING = 'pending',
  PARTIAL = 'partial',
  COMPLETE = 'complete',
  BACKORDERED = 'backordered'
}

export enum AlertType {
  LOW_STOCK = 'low_stock',
  EXPIRING = 'expiring',
  OVERSTOCK = 'overstock',
  QUALITY = 'quality'
}

export enum AlertSeverity {
  INFO = 'info',
  WARNING = 'warning',
  CRITICAL = 'critical'
}