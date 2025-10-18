# backend/app/models/inventory.py 

from sqlalchemy import (Text, DateTime, Float, Integer, String, Boolean, ForeignKey, 
                       Numeric, CheckConstraint, LargeBinary)
from sqlalchemy.dialects.postgresql import JSON as JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import BaseModel
from .lookups import (
    ProductType, InventoryTransactionType, PurchaseOrderStatus, 
    InventoryAdjustmentType
)
from . import db

class Product(BaseModel):
    __tablename__ = 'products'
    
    # Foreign keys
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=True)
    
    # Lookup foreign key
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    
    # Product identification
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    
    # Product details
    unit_of_measure = db.Column(db.String(50), nullable=False)
    unit_size = db.Column(db.String(50))
    weight = db.Column(Numeric(10, 2))
    dimensions = db.Column(db.String(100))
    
    # Pricing
    cost_price = db.Column(Numeric(10, 2), nullable=False)
    selling_price = db.Column(Numeric(10, 2), nullable=False)
    current_price = db.Column(Numeric(10, 2), nullable=False)
    tax_rate = db.Column(Numeric(5, 2), default=0.0)
    discount_percentage = db.Column(Numeric(5, 2), default=0.0)
    
    # Inventory management
    min_stock_level = db.Column(db.Integer, default=0)
    max_stock_level = db.Column(db.Integer, default=0)
    reorder_point = db.Column(db.Integer, default=0)
    current_stock = db.Column(db.Integer, default=0)
    reserved_stock = db.Column(db.Integer, default=0)
    average_consumption = db.Column(db.Integer, default=0)
    
    # Medical specific fields
    is_medical = db.Column(db.Boolean, default=False)
    requires_prescription = db.Column(db.Boolean, default=False)
    active_ingredients = db.Column(db.Text)
    dosage_form = db.Column(db.String(100))
    strength = db.Column(db.String(100))
    
    # Expiration and shelf life
    expiration_alert_days = db.Column(db.Integer, default=30)
    shelf_life_months = db.Column(db.Integer)
    requires_refrigeration = db.Column(db.Boolean, default=False)
    
    # Status and tracking
    status = db.Column(db.String(20), default='active')
    is_taxable = db.Column(db.Boolean, default=True)
    is_returnable = db.Column(db.Boolean, default=False)
    return_period_days = db.Column(db.Integer, default=30)
    
    # Barcode and identification
    barcode = db.Column(db.String(100), unique=True, index=True)
    manufacturer_code = db.Column(db.String(100))
    supplier_code = db.Column(db.String(100))
    ndc_code = db.Column(db.String(100))
    
    # Relationships
    organization = db.relationship('Organization', back_populates='products')
    supplier = db.relationship('Supplier', back_populates='products')
    category = db.relationship('ProductCategory', back_populates='products')
    product_type = relationship('ProductType')
    images = db.relationship('ProductImage', back_populates='product', cascade='all, delete-orphan')
    price_history = db.relationship('ProductPriceHistory', back_populates='product', cascade='all, delete-orphan')
    inventory_transactions = db.relationship('InventoryTransaction', back_populates='product')

    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint('selling_price >= cost_price', name='check_selling_price_gte_cost'),
        CheckConstraint('current_stock >= 0', name='check_current_stock_positive'),
        CheckConstraint('reserved_stock >= 0', name='check_reserved_stock_positive'),
        CheckConstraint('min_stock_level >= 0', name='check_min_stock_positive'),
        CheckConstraint('max_stock_level >= min_stock_level', name='check_max_stock_gte_min'),
        db.Index('idx_product_sku_org', 'sku', 'organization_id'),
        db.Index('idx_product_name_org', 'name', 'organization_id'),
        db.Index('idx_product_type_status', 'product_type_id', 'status'),
        db.Index('idx_product_stock_level', 'current_stock'),
        db.Index('idx_product_barcode', 'barcode'),
    )

    @property
    def available_stock(self):
        """Calculate available stock (current stock - reserved stock)"""
        return max(0, self.current_stock - self.reserved_stock)

    @property
    def needs_reorder(self):
        """Check if product needs reorder"""
        return self.available_stock <= self.reorder_point

    @property
    def total_value(self):
        """Calculate total inventory value"""
        return float(self.current_stock) * float(self.cost_price)

    @property
    def stock_status(self):
        """Get stock status description"""
        if self.current_stock <= 0:
            return 'out_of_stock'
        elif self.needs_reorder:
            return 'low_stock'
        elif self.current_stock > self.max_stock_level:
            return 'overstock'
        else:
            return 'adequate'

    def _to_dict_impl(self):
        return {
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'brand': self.brand,
            'product_type': self.product_type.to_dict() if self.product_type else None,
            'unit_of_measure': self.unit_of_measure,
            'unit_size': self.unit_size,
            'cost_price': float(self.cost_price) if self.cost_price else None,
            'selling_price': float(self.selling_price) if self.selling_price else None,
            'current_price': float(self.current_price) if self.current_price else None,
            'current_stock': self.current_stock,
            'available_stock': self.available_stock,
            'reserved_stock': self.reserved_stock,
            'min_stock_level': self.min_stock_level,
            'max_stock_level': self.max_stock_level,
            'reorder_point': self.reorder_point,
            'status': self.status,
            'stock_status': self.stock_status,
            'is_medical': self.is_medical,
            'requires_prescription': self.requires_prescription,
            'barcode': self.barcode,
            'category': self.category.name if self.category else None,
            'supplier': self.supplier.name if self.supplier else None,
            'total_value': self.total_value
        }

    def update_stock(self, quantity, transaction_type_id, reference_id=None, notes=None, user_id=None):
        """Update stock levels and create transaction record"""
        old_stock = self.current_stock
        
        # Get transaction type
        transaction_type = InventoryTransactionType.query.get(transaction_type_id)
        if not transaction_type:
            return None
            
        # Update stock based on transaction type
        if transaction_type.stock_direction == 'in':
            self.current_stock += quantity
        elif transaction_type.stock_direction == 'out':
            self.current_stock = max(0, self.current_stock - quantity)
        
        # Create transaction record
        transaction = InventoryTransaction(
            product_id=self.id,
            transaction_type_id=transaction_type_id,
            quantity=quantity,
            old_stock_level=old_stock,
            new_stock_level=self.current_stock,
            unit_cost=self.cost_price,
            total_cost=quantity * self.cost_price,
            reference_type=self.__class__.__name__,
            reference_id=reference_id,
            notes=notes,
            performed_by=user_id
        )
        
        return transaction

    def reserve_stock(self, quantity):
        """Reserve stock for orders"""
        if quantity <= self.available_stock:
            self.reserved_stock += quantity
            return True
        return False

    def release_stock(self, quantity):
        """Release reserved stock"""
        if quantity <= self.reserved_stock:
            self.reserved_stock -= quantity
            return True
        return False

    def get_stock_movement(self, days=30):
        """Get stock movement history for specified days"""
        from datetime import timedelta
        since_date = datetime.utcnow() - timedelta(days=days)
        
        transactions = InventoryTransaction.query.filter(
            InventoryTransaction.product_id == self.id,
            InventoryTransaction.created_at >= since_date
        ).order_by(InventoryTransaction.created_at.desc()).all()
        
        return transactions

    @classmethod
    def get_low_stock_items(cls, organization_id):
        """Get products that need reorder"""
        return cls.query.filter(
            cls.organization_id == organization_id,
            cls.is_active == True,
            cls.current_stock <= cls.reorder_point
        ).all()

    @classmethod
    def get_expiring_soon(cls, organization_id, days=30):
        """Get products expiring soon (for medications)"""
        # This would need additional expiration date field
        # For now, return empty list as placeholder
        return []

    def __repr__(self):
        return f'<Product {self.sku} - {self.name}>'

class ProductCategory(BaseModel):
    __tablename__ = 'product_categories'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=True)
    
    # Relationships
    organization = relationship('Organization', backref='product_categories')
    parent = relationship('ProductCategory', 
                         remote_side='ProductCategory.id', 
                         backref='subcategories',
                         foreign_keys=[parent_category_id])
    products = db.relationship('Product', back_populates='category', lazy=True)

    __table_args__ = (
        db.Index('idx_category_org_name', 'organization_id', 'name'),
        db.Index('idx_category_parent', 'parent_category_id'),
    )

    def _to_dict_impl(self):
        return {
            'name': self.name,
            'description': self.description,
            'parent_category_id': self.parent_category_id,
            'subcategories_count': len(self.subcategories) if self.subcategories else 0,
            'products_count': len(self.products) if self.products else 0,
            'full_path': self.full_path
        }

    @property
    def full_path(self):
        """Get full category path"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent
        return ' > '.join(path)

class ProductImage(BaseModel):
    __tablename__ = 'product_images'
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    
    product = db.relationship('Product', back_populates='images')

    __table_args__ = (
        db.Index('idx_product_image_product', 'product_id'),
        db.Index('idx_product_image_primary', 'is_primary'),
    )

    def _to_dict_impl(self):
        return {
            'image_url': self.image_url,
            'caption': self.caption,
            'is_primary': self.is_primary,
            'sort_order': self.sort_order
        }

class ProductPriceHistory(BaseModel):
    __tablename__ = 'product_price_history'
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    old_price = db.Column(Numeric(10, 2), nullable=False)
    new_price = db.Column(Numeric(10, 2), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    change_reason = db.Column(db.Text)
    effective_date = db.Column(DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', back_populates='price_history')
    user = relationship('User')
    
    __table_args__ = (
        db.Index('idx_price_history_product', 'product_id'),
        db.Index('idx_price_history_date', 'effective_date'),
    )

    def _to_dict_impl(self):
        return {
            'old_price': float(self.old_price) if self.old_price else None,
            'new_price': float(self.new_price) if self.new_price else None,
            'change_reason': self.change_reason,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'changed_by_user': f"{self.user.first_name} {self.user.last_name}" if self.user else None
        }

class Supplier(BaseModel):
    __tablename__ = 'suppliers'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    
    # Address information
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='USA')
    
    # Business information
    tax_id = db.Column(db.String(100))
    payment_terms = db.Column(db.String(100))
    lead_time_days = db.Column(db.Integer, default=7)
    rating = db.Column(db.Integer)
    
    # Status
    is_preferred = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Additional info
    website = db.Column(db.String(200))
    notes = db.Column(db.Text)
    categories_served = db.Column(JSONB)
    
    # Relationships
    organization = relationship('Organization', back_populates='suppliers')
    products = db.relationship('Product', back_populates='supplier')
    purchase_orders = relationship('PurchaseOrder', back_populates='supplier')
    
    __table_args__ = (
        db.Index('idx_supplier_org_name', 'organization_id', 'name'),
        db.Index('idx_supplier_status', 'is_active'),
        db.Index('idx_supplier_preferred', 'is_preferred'),
    )

    def _to_dict_impl(self):
        return {
            'name': self.name,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'payment_terms': self.payment_terms,
            'lead_time_days': self.lead_time_days,
            'rating': self.rating,
            'is_preferred': self.is_preferred,
            'website': self.website,
            'categories_served': self.categories_served or [],
            'total_spend': self.total_spend
        }

    @property
    def total_spend(self):
        """Calculate total spend with this supplier"""
        total = 0.0
        for po in self.purchase_orders:
            if po.status and po.status.code == 'received':
                total += float(po.total_amount) if po.total_amount else 0.0
        return total

    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        return self.rating or 0

    def get_recent_orders(self, limit=10):
        """Get recent purchase orders"""
        return PurchaseOrder.query.filter_by(
            supplier_id=self.id
        ).order_by(PurchaseOrder.created_at.desc()).limit(limit).all()

class PurchaseOrder(BaseModel):
    __tablename__ = 'purchase_orders'
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    
    # Lookup foreign key
    status_id = db.Column(db.Integer, db.ForeignKey('purchase_order_statuses.id'), nullable=False)
    
    # Order information
    po_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    order_date = db.Column(DateTime, default=datetime.utcnow)
    expected_delivery_date = db.Column(DateTime)
    actual_delivery_date = db.Column(DateTime)
    
    # Status and tracking
    tracking_number = db.Column(db.String(100))
    shipping_method = db.Column(db.String(100))
    
    # Financial information
    subtotal = db.Column(Numeric(10, 2), default=0.0)
    tax_amount = db.Column(Numeric(10, 2), default=0.0)
    shipping_cost = db.Column(Numeric(10, 2), default=0.0)
    total_amount = db.Column(Numeric(10, 2), nullable=False)
    
    # Notes and terms
    notes = db.Column(db.Text)
    terms_and_conditions = db.Column(db.Text)
    
    # Audit
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(DateTime)
    
    # Relationships
    supplier = relationship('Supplier', back_populates='purchase_orders')
    organization = relationship('Organization', back_populates='purchase_orders')
    creator = relationship('User', foreign_keys=[created_by])
    approver = relationship('User', foreign_keys=[approved_by])
    items = relationship('PurchaseOrderItem', back_populates='purchase_order', cascade='all, delete-orphan')
    status = relationship('PurchaseOrderStatus')
    
    __table_args__ = (
        db.Index('idx_po_org_status', 'organization_id', 'status_id'),
        db.Index('idx_po_supplier_date', 'supplier_id', 'order_date'),
        db.Index('idx_po_number', 'po_number'),
        db.Index('idx_po_delivery_date', 'expected_delivery_date'),
    )

    def _to_dict_impl(self):
        return {
            'po_number': self.po_number,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'expected_delivery_date': self.expected_delivery_date.isoformat() if self.expected_delivery_date else None,
            'actual_delivery_date': self.actual_delivery_date.isoformat() if self.actual_delivery_date else None,
            'status': self.status.to_dict() if self.status else None,
            'subtotal': float(self.subtotal) if self.subtotal else None,
            'tax_amount': float(self.tax_amount) if self.tax_amount else None,
            'shipping_cost': float(self.shipping_cost) if self.shipping_cost else None,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'supplier': self.supplier.name if self.supplier else None,
            'items_count': len(self.items) if self.items else 0,
            'items': [item.to_dict() for item in self.items] if self.items else []
        }

    def calculate_totals(self):
        """Calculate order totals from items"""
        self.subtotal = sum(float(item.total_cost) for item in self.items)
        self.total_amount = self.subtotal + float(self.tax_amount) + float(self.shipping_cost)

    def add_item(self, product, quantity, unit_cost, notes=None):
        """Add item to purchase order"""
        item = PurchaseOrderItem(
            purchase_order_id=self.id,
            product_id=product.id,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=quantity * unit_cost,
            notes=notes
        )
        self.items.append(item)
        self.calculate_totals()
        return item

    def mark_received(self, received_by, actual_delivery_date=None):
        """Mark purchase order as received"""
        received_status = PurchaseOrderStatus.query.filter_by(code='received').first()
        if received_status:
            self.status_id = received_status.id
            self.actual_delivery_date = actual_delivery_date or datetime.utcnow()
            
            # Update inventory for each item
            purchase_transaction_type = InventoryTransactionType.query.filter_by(code='purchase').first()
            
            for item in self.items:
                if purchase_transaction_type:
                    item.product.update_stock(
                        quantity=item.quantity,
                        transaction_type_id=purchase_transaction_type.id,
                        reference_id=self.id,
                        notes=f"PO #{self.po_number}",
                        user_id=received_by
                    )

    def get_receipt_status(self):
        """Get receipt status summary"""
        received_items = sum(1 for item in self.items if item.received_quantity > 0)
        total_items = len(self.items)
        
        return {
            'received_items': received_items,
            'total_items': total_items,
            'completion_rate': (received_items / total_items * 100) if total_items > 0 else 0
        }

class PurchaseOrderItem(BaseModel):
    __tablename__ = 'purchase_order_items'
    
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'))  # ✅ THIS IS CRITICAL
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item details
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(Numeric(10, 2), nullable=False)
    total_cost = db.Column(Numeric(10, 2), nullable=False)
    
    # Receipt information
    received_quantity = db.Column(db.Integer, default=0)
    received_date = db.Column(DateTime)
    
    # Additional info
    notes = db.Column(db.Text)
    
    # Relationships
    purchase_order = relationship('PurchaseOrder', back_populates='items')
    product = relationship('Product')
    inventory_item = db.relationship('InventoryItem', back_populates='purchase_order_items')
        
    __table_args__ = (
        db.Index('idx_po_item_po_product', 'purchase_order_id', 'product_id'),
        CheckConstraint('received_quantity <= quantity', name='check_received_quantity'),
    )

    def _to_dict_impl(self):
        return {
            'product_name': self.product.name if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'quantity': self.quantity,
            'received_quantity': self.received_quantity,
            'unit_cost': float(self.unit_cost) if self.unit_cost else None,
            'total_cost': float(self.total_cost) if self.total_cost else None,
            'notes': self.notes,
            'is_fully_received': self.received_quantity >= self.quantity
        }

    def mark_received(self, quantity, received_date=None):
        """Mark item as received"""
        if quantity <= (self.quantity - self.received_quantity):
            self.received_quantity += quantity
            self.received_date = received_date or datetime.utcnow()
            return True
        return False

class InventoryItem(BaseModel):
    __tablename__ = 'inventory_items'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    name = db.Column(db.String(200), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    
    # Inventory details
    unit_price = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    min_quantity = db.Column(db.Integer, default=0, nullable=False)
    max_quantity = db.Column(db.Integer, default=1000, nullable=False)
    
    # Financial information
    cost = db.Column(Numeric(10, 2), nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)
    
    # Supplier information
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    location = db.Column(db.String(100))
    
    # Status
    reorder_point = db.Column(db.Integer)
    lead_time_days = db.Column(db.Integer)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='inventory_items')
    supplier = db.relationship('Supplier', backref='supplier_inventory_items')
    purchase_order_items = db.relationship('PurchaseOrderItem', back_populates='inventory_item', cascade='all, delete-orphan') #  lazy=True)
    adjustments = db.relationship('InventoryAdjustment', back_populates='item')
    inventory_transactions = db.relationship(
        "InventoryTransaction",
        back_populates="transaction_item",
        lazy=True,
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.Index('idx_inventory_item_org_sku', 'organization_id', 'sku'),
        db.Index('idx_inventory_item_name', 'name'),
        db.Index('idx_inventory_item_category', 'category'),
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
    )

    def _to_dict_impl(self):
        return {
            'name': self.name,
            'category': self.category,
            'sku': self.sku,
            'description': self.description,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'min_quantity': self.min_quantity,
            'max_quantity': self.max_quantity,
            'cost': float(self.cost) if self.cost else None,
            'price': float(self.price) if self.price else None,
            'location': self.location,
            'reorder_point': self.reorder_point,
            'lead_time_days': self.lead_time_days,
            'total_value': float(self.quantity * self.cost) if self.cost else 0.0,
            'stock_status': self.get_stock_status(),
            'supplier': self.supplier.name if self.supplier else None
        }

    def get_stock_status(self):
        if self.quantity <= 0:
            return 'out_of_stock'
        elif self.reorder_point and self.quantity <= self.reorder_point:
            return 'low_stock'
        elif self.max_quantity and self.quantity > self.max_quantity:
            return 'overstock'
        return 'adequate'

    def needs_reorder(self):
        return self.reorder_point is not None and self.quantity <= self.reorder_point

class InventoryTransaction(BaseModel):
    __tablename__ = 'inventory_transactions'
    
    # Link directly to InventoryItem
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('inventory_transaction_types.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    # Stock levels before and after transaction
    old_stock_level = db.Column(db.Integer, nullable=False)
    new_stock_level = db.Column(db.Integer, nullable=False)
    
    # Financial information
    unit_cost = db.Column(Numeric(10, 2), nullable=False)
    total_cost = db.Column(Numeric(10, 2), nullable=False)
    
    # Reference information
    reference_type = db.Column(db.String(50))
    reference_id = db.Column(db.Integer)
    
    # Additional details
    notes = db.Column(db.Text)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    transaction_performer = db.relationship(
        'User',
        foreign_keys=[performed_by],
        back_populates='user_inventory_transactions'
    )
    transaction_item = db.relationship(
        'InventoryItem',
        back_populates='inventory_transactions'
    )
    transaction_type = relationship('InventoryTransactionType')
    product = relationship('Product')
    
    __table_args__ = (
        db.Index('idx_inventory_txn_item_date', 'item_id', 'created_at'),
        db.Index('idx_inventory_txn_type', 'transaction_type_id'),
        db.Index('idx_inventory_txn_reference', 'reference_type', 'reference_id'),
    )

    def _to_dict_impl(self):
        return {
            'transaction_type': self.transaction_type.to_dict() if self.transaction_type else None,
            'quantity': self.quantity,
            'old_stock_level': self.old_stock_level,
            'new_stock_level': self.new_stock_level,
            'unit_cost': float(self.unit_cost) if self.unit_cost else None,
            'total_cost': float(self.total_cost) if self.total_cost else None,
            'reference_type': self.reference_type,
            'reference_id': self.reference_id,
            'notes': self.notes,
            'performed_by_user': f"{self.transaction_performer.first_name} {self.transaction_performer.last_name}" if self.transaction_performer else None,
            'item': self.transaction_item.name if self.transaction_item else None,
            'product': self.product.name if self.product else None
        }

class InventoryAdjustment(BaseModel):
    __tablename__ = 'inventory_adjustments'
    
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    adjustment_type_id = db.Column(db.Integer, db.ForeignKey('inventory_adjustment_types.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text)
    adjusted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    adjustment_date = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    item = relationship('InventoryItem', back_populates='adjustments')
    user = relationship('User')
    adjustment_type = relationship('InventoryAdjustmentType')
    
    __table_args__ = (
        db.Index('idx_inventory_adj_item_date', 'item_id', 'adjustment_date'),
        db.Index('idx_inventory_adj_type', 'adjustment_type_id'),
    )

    def _to_dict_impl(self):
        return {
            'adjustment_type': self.adjustment_type.to_dict() if self.adjustment_type else None,
            'quantity': self.quantity,
            'reason': self.reason,
            'adjustment_date': self.adjustment_date.isoformat() if self.adjustment_date else None,
            'adjusted_by_user': f"{self.user.first_name} {self.user.last_name}" if self.user else None,
            'item_name': self.item.name if self.item else None
        }

    def apply_adjustment(self):
        """Apply the adjustment to inventory"""
        if self.adjustment_type.stock_impact == 'increase':
            self.item.quantity += self.quantity
        elif self.adjustment_type.stock_impact == 'decrease':
            self.item.quantity = max(0, self.item.quantity - self.quantity)
        
        # Create transaction record
        adjustment_transaction_type = InventoryTransactionType.query.filter_by(code='adjustment').first()
        if adjustment_transaction_type:
            transaction = InventoryTransaction(
                item_id=self.item_id,
                transaction_type_id=adjustment_transaction_type.id,
                quantity=self.quantity,
                old_stock_level=self.item.quantity - self.quantity,
                new_stock_level=self.item.quantity,
                unit_cost=self.item.cost,
                total_cost=self.quantity * self.item.cost,
                reference_type='InventoryAdjustment',
                reference_id=self.id,
                notes=f"Adjustment: {self.reason}",
                performed_by=self.adjusted_by
            )
            
            return transaction
        return None


