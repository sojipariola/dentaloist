# backend/app/routes/inventory.py

from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_, desc
from decimal import Decimal, ROUND_HALF_UP
import json
from sqlalchemy.sql import case
from ..models import (
    db, InventoryItem, InventoryTransaction, Supplier, 
    User, Organization, PurchaseOrder, InventoryAdjustment
)
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit
from ..utils.validation import validate_inventory_item_data, validate_inventory_transaction_data

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')

# ===== Inventory Item Routes =====

@inventory_bp.route('/items', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_inventory', 'manage_inventory'])
@rate_limit(limit=60, period=60)
def get_inventory_items():
    """
    Get paginated inventory items with advanced filtering and search
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        category = request.args.get('category')
        supplier_id = request.args.get('supplier_id')
        low_stock = request.args.get('low_stock', 'false').lower() == 'true'
        out_of_stock = request.args.get('out_of_stock', 'false').lower() == 'true'
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'name')
        sort_order = request.args.get('sort_order', 'asc')
        
        query = multi_tenant_query(InventoryItem)
        
        # Apply filters
        if category and category != 'all':
            query = query.filter(InventoryItem.category == category)
        
        if supplier_id:
            query = query.filter(InventoryItem.supplier_id == supplier_id)
        
        if low_stock:
            query = query.filter(InventoryItem.quantity <= InventoryItem.min_quantity)
        
        if out_of_stock:
            query = query.filter(InventoryItem.quantity == 0)
        
        if search:
            search_filter = or_(
                InventoryItem.name.ilike(f'%{search}%'),
                InventoryItem.sku.ilike(f'%{search}%'),
                InventoryItem.description.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        # Apply sorting
        sort_column = getattr(InventoryItem, sort_by, InventoryItem.name)
        if sort_order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)
        
        items = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Get inventory statistics
        stats = db.session.query(
            func.count(InventoryItem.id),
            func.sum(InventoryItem.quantity * InventoryItem.cost),
            func.sum(case([(InventoryItem.quantity <= InventoryItem.min_quantity, 1)], else_=0)),
            func.sum(case([(InventoryItem.quantity == 0, 1)], else_=0))
        ).filter(InventoryItem.organization_id == g.tenant_id).first()
        
        return jsonify({
            'items': [item.to_dict(include_supplier=True) for item in items.items],
            'pagination': {
                'total': items.total,
                'pages': items.pages,
                'current_page': page,
                'per_page': per_page
            },
            'statistics': {
                'total_items': stats[0] or 0,
                'total_value': float(stats[1] or 0),
                'low_stock_items': stats[2] or 0,
                'out_of_stock_items': stats[3] or 0
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching inventory items: {str(e)}")
        return jsonify({'error': 'Failed to fetch inventory items'}), 500

@inventory_bp.route('/items/<int:item_id>', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_inventory', 'manage_inventory'])
def get_inventory_item(item_id):
    """
    Get detailed inventory item information including transaction history
    """
    try:
        item = multi_tenant_query(InventoryItem).filter_by(id=item_id).first_or_404()
        
        # Get recent transactions
        recent_transactions = InventoryTransaction.query.filter_by(
            item_id=item_id
        ).order_by(InventoryTransaction.created_at.desc()).limit(10).all()
        
        # Get usage statistics
        usage_stats = db.session.query(
            InventoryTransaction.type,
            func.sum(InventoryTransaction.quantity),
            func.sum(InventoryTransaction.total_cost)
        ).filter_by(item_id=item_id).group_by(InventoryTransaction.type).all()
        
        return jsonify({
            'item': item.to_dict(include_supplier=True),
            'recent_transactions': [txn.to_dict() for txn in recent_transactions],
            'usage_statistics': {
                txn_type: {'quantity': float(quantity or 0), 'cost': float(cost or 0)}
                for txn_type, quantity, cost in usage_stats
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching inventory item {item_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch inventory item'}), 500

@inventory_bp.route('/items', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_inventory'])
def create_inventory_item():
    """
    Create a new inventory item with validation
    """
    try:
        data = request.get_json()
        
        # Validate inventory item data
        validation_error = validate_inventory_item_data(data)
        if validation_error:
            return validation_error
        
        # Verify supplier belongs to current tenant if provided
        if data.get('supplier_id'):
            supplier = multi_tenant_query(Supplier).filter_by(id=data['supplier_id']).first()
            if not supplier:
                return jsonify({'error': 'Supplier not found or access denied'}), 404
        
        # Generate SKU if not provided
        sku = data.get('sku')
        if not sku:
            sku = generate_sku(data['name'], data['category'])
        
        # Check for duplicate SKU
        existing_item = InventoryItem.query.filter_by(
            organization_id=g.tenant_id,
            sku=sku
        ).first()
        
        if existing_item:
            return jsonify({'error': 'SKU already exists'}), 400
        
        item = InventoryItem(
            organization_id=g.tenant_id,
            name=data['name'],
            category=data['category'],
            sku=sku,
            unit=data['unit'],
            quantity=data.get('quantity', 0),
            min_quantity=data.get('min_quantity', 0),
            max_quantity=data.get('max_quantity', 1000),
            cost=Decimal(str(data['cost'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            price=Decimal(str(data['price'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            description=data.get('description'),
            supplier_id=data.get('supplier_id'),
            location=data.get('location'),
            is_active=data.get('is_active', True),
            reorder_point=data.get('reorder_point'),
            lead_time_days=data.get('lead_time_days')
        )
        
        db.session.add(item)
        db.session.commit()
        
        # Log the creation
        current_app.logger.info(f"Inventory item created: {item.name} (ID: {item.id}) by user {g.user.id}")
        
        return jsonify({
            'message': 'Inventory item created successfully',
            'item': item.to_dict(include_supplier=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating inventory item: {str(e)}")
        return jsonify({'error': 'Failed to create inventory item'}), 500

@inventory_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
@tenant_required
@permission_required(['manage_inventory'])
def update_inventory_item(item_id):
    """
    Update an existing inventory item
    """
    try:
        item = multi_tenant_query(InventoryItem).filter_by(id=item_id).first_or_404()
        data = request.get_json()
        
        # Validate update data
        validation_error = validate_inventory_item_data(data, is_update=True)
        if validation_error:
            return validation_error
        
        # Verify supplier belongs to current tenant if provided
        if data.get('supplier_id'):
            supplier = multi_tenant_query(Supplier).filter_by(id=data['supplier_id']).first()
            if not supplier:
                return jsonify({'error': 'Supplier not found or access denied'}), 404
        
        # Check for duplicate SKU if changing
        if data.get('sku') and data['sku'] != item.sku:
            existing_item = InventoryItem.query.filter_by(
                organization_id=g.tenant_id,
                sku=data['sku']
            ).first()
            
            if existing_item and existing_item.id != item_id:
                return jsonify({'error': 'SKU already exists'}), 400
        
        # Update allowed fields
        allowed_fields = [
            'name', 'category', 'sku', 'unit', 'min_quantity', 'max_quantity',
            'cost', 'price', 'description', 'supplier_id', 'location',
            'is_active', 'reorder_point', 'lead_time_days'
        ]
        
        for field in allowed_fields:
            if field in data:
                if field in ['cost', 'price']:
                    setattr(item, field, Decimal(str(data[field])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                else:
                    setattr(item, field, data[field])
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Inventory item updated successfully',
            'item': item.to_dict(include_supplier=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating inventory item {item_id}: {str(e)}")
        return jsonify({'error': 'Failed to update inventory item'}), 500

@inventory_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
@tenant_required
@permission_required(['manage_inventory'])
def delete_inventory_item(item_id):
    """
    Delete an inventory item (soft delete)
    """
    try:
        item = multi_tenant_query(InventoryItem).filter_by(id=item_id).first_or_404()
        
        # Check if item has transactions
        transaction_count = InventoryTransaction.query.filter_by(item_id=item_id).count()
        if transaction_count > 0:
            return jsonify({
                'error': 'Cannot delete item with transaction history. Archive instead.',
                'transaction_count': transaction_count
            }), 400
        
        # Soft delete
        item.is_active = False
        item.deleted_at = datetime.utcnow()
        db.session.commit()
        
        current_app.logger.info(f"Inventory item deleted: {item.name} (ID: {item_id}) by user {g.user.id}")
        
        return jsonify({'message': 'Inventory item deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting inventory item {item_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete inventory item'}), 500

# ===== Inventory Transaction Routes =====

@inventory_bp.route('/transactions', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_inventory', 'manage_inventory'])
def get_inventory_transactions():
    """
    Get paginated inventory transactions with filtering
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        item_id = request.args.get('item_id')
        transaction_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = multi_tenant_query(InventoryTransaction).join(InventoryItem)
        
        # Apply filters
        if item_id:
            query = query.filter(InventoryTransaction.item_id == item_id)
        
        if transaction_type and transaction_type != 'all':
            query = query.filter(InventoryTransaction.type == transaction_type)
        
        if start_date:
            try:
                start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.filter(InventoryTransaction.created_at >= start_date_obj)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format'}), 400
        
        if end_date:
            try:
                end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.filter(InventoryTransaction.created_at <= end_date_obj)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format'}), 400
        
        # Order by most recent
        transactions = query.order_by(desc(InventoryTransaction.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'transactions': [txn.to_dict(include_item=True) for txn in transactions.items],
            'pagination': {
                'total': transactions.total,
                'pages': transactions.pages,
                'current_page': page,
                'per_page': per_page
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching inventory transactions: {str(e)}")
        return jsonify({'error': 'Failed to fetch inventory transactions'}), 500

@inventory_bp.route('/transactions', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_inventory'])
def create_inventory_transaction():
    """
    Create an inventory transaction (purchase, sale, adjustment, transfer)
    """
    try:
        data = request.get_json()
        
        # Validate transaction data
        validation_error = validate_inventory_transaction_data(data)
        if validation_error:
            return validation_error
        
        # Verify item belongs to current tenant
        item = multi_tenant_query(InventoryItem).filter_by(id=data['item_id']).first()
        if not item:
            return jsonify({'error': 'Inventory item not found or access denied'}), 404
        
        # Check stock availability for sales
        if data['type'] == 'sale' and item.quantity < data['quantity']:
            return jsonify({
                'error': 'Insufficient stock',
                'available': item.quantity,
                'requested': data['quantity']
            }), 400
        
        # Calculate costs
        unit_cost = Decimal(str(data.get('unit_cost', item.cost)))
        total_cost = unit_cost * Decimal(str(data['quantity']))
        
        transaction = InventoryTransaction(
            item_id=data['item_id'],
            type=data['type'],
            quantity=data['quantity'],
            unit_cost=unit_cost,
            total_cost=total_cost,
            reference_type=data.get('reference_type'),
            reference_id=data.get('reference_id'),
            notes=data.get('notes'),
            performed_by=g.user.id
        )
        
        # Update item quantity
        if data['type'] == 'purchase':
            item.quantity += data['quantity']
        elif data['type'] == 'sale':
            item.quantity -= data['quantity']
        elif data['type'] == 'adjustment':
            item.quantity = data['quantity']  # Set to specific quantity
        
        # Update item cost if this is a purchase and cost is provided
        if data['type'] == 'purchase' and data.get('unit_cost'):
            # Weighted average cost calculation
            total_value = (item.quantity * item.cost) + total_cost
            new_quantity = item.quantity + data['quantity']
            item.cost = (total_value / new_quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        db.session.add(transaction)
        db.session.commit()
        
        # Check if item needs reordering
        if item.quantity <= item.reorder_point:
            current_app.logger.info(f"Item {item.name} (ID: {item.id}) needs reordering")
        
        return jsonify({
            'message': 'Inventory transaction recorded successfully',
            'transaction': transaction.to_dict(include_item=True),
            'new_quantity': item.quantity
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating inventory transaction: {str(e)}")
        return jsonify({'error': 'Failed to create inventory transaction'}), 500

# ===== Inventory Reports and Analytics =====

@inventory_bp.route('/reports/summary', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_inventory'])
def get_inventory_summary():
    """
    Get inventory summary and analytics
    """
    try:
        # Total inventory value
        total_value = db.session.query(
            func.sum(InventoryItem.quantity * InventoryItem.cost)
        ).filter(InventoryItem.organization_id == g.tenant_id).scalar() or 0
        
        # Category breakdown
        category_breakdown = db.session.query(
            InventoryItem.category,
            func.count(InventoryItem.id),
            func.sum(InventoryItem.quantity),
            func.sum(InventoryItem.quantity * InventoryItem.cost)
        ).filter(InventoryItem.organization_id == g.tenant_id).group_by(InventoryItem.category).all()
        
        # Low stock items
        low_stock_items = multi_tenant_query(InventoryItem).filter(
            InventoryItem.quantity <= InventoryItem.min_quantity,
            InventoryItem.quantity > 0
        ).count()
        
        # Out of stock items
        out_of_stock_items = multi_tenant_query(InventoryItem).filter(
            InventoryItem.quantity == 0
        ).count()
        
        # Recent transactions
        recent_transactions = multi_tenant_query(InventoryTransaction).join(InventoryItem).order_by(
            desc(InventoryTransaction.created_at)
        ).limit(5).all()
        
        return jsonify({
            'summary': {
                'total_value': float(total_value),
                'total_items': multi_tenant_query(InventoryItem).count(),
                'low_stock_items': low_stock_items,
                'out_of_stock_items': out_of_stock_items,
                'total_categories': len(category_breakdown)
            },
            'category_breakdown': [
                {
                    'category': category,
                    'item_count': count,
                    'total_quantity': float(quantity or 0),
                    'total_value': float(value or 0)
                }
                for category, count, quantity, value in category_breakdown
            ],
            'recent_transactions': [txn.to_dict(include_item=True) for txn in recent_transactions]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating inventory report: {str(e)}")
        return jsonify({'error': 'Failed to generate inventory report'}), 500

@inventory_bp.route('/reports/valuation', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_inventory'])
def get_inventory_valuation():
    """
    Get detailed inventory valuation report
    """
    try:
        valuation_method = request.args.get('method', 'fifo')  # fifo, lifo, weighted_average
        
        # This would be a more complex implementation in a real system
        # For now, return basic valuation
        items = multi_tenant_query(InventoryItem).all()
        
        valuation_data = []
        total_valuation = 0
        
        for item in items:
            item_value = float(item.quantity * item.cost)
            total_valuation += item_value
            
            valuation_data.append({
                'item_id': item.id,
                'name': item.name,
                'sku': item.sku,
                'quantity': item.quantity,
                'unit_cost': float(item.cost),
                'total_value': item_value,
                'category': item.category
            })
        
        return jsonify({
            'valuation_method': valuation_method,
            'total_valuation': total_valuation,
            'items': sorted(valuation_data, key=lambda x: x['total_value'], reverse=True),
            'as_of': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error generating inventory valuation: {str(e)}")
        return jsonify({'error': 'Failed to generate inventory valuation'}), 500

# ===== Helper Functions =====

def generate_sku(name, category):
    """
    Generate a SKU from item name and category
    """
    import re
    from datetime import datetime
    
    # Clean the name and category
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', name.upper())[:3]
    clean_category = re.sub(r'[^a-zA-Z0-9]', '', category.upper())[:2]
    
    # Add timestamp for uniqueness
    timestamp = datetime.utcnow().strftime('%m%d%H%M')
    
    return f"{clean_category}-{clean_name}-{timestamp}"

def validate_inventory_item_data(data, is_update=False):
    """Validate inventory item data"""
    if not is_update:
        required_fields = ['name', 'category', 'unit', 'cost', 'price']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'message': f'The following fields are required: {", ".join(missing_fields)}'
            }), 400
    
    # Validate numeric fields
    numeric_fields = ['quantity', 'min_quantity', 'max_quantity', 'cost', 'price']
    for field in numeric_fields:
        if field in data:
            try:
                value = Decimal(str(data[field]))
                if value < 0:
                    return jsonify({'error': f'{field.replace("_", " ").title()} cannot be negative'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid {field.replace("_", " ")} format'}), 400
    
    # Validate that min_quantity <= max_quantity
    if data.get('min_quantity') and data.get('max_quantity'):
        if data['min_quantity'] > data['max_quantity']:
            return jsonify({'error': 'Minimum quantity cannot exceed maximum quantity'}), 400
    
    return None

def validate_inventory_transaction_data(data):
    """Validate inventory transaction data"""
    required_fields = ['item_id', 'type', 'quantity']
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field.replace('_', ' ').Title())
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields,
            'message': f'The following fields are required: {", ".join(missing_fields)}'
        }), 400
    
    # Validate transaction type
    valid_types = ['purchase', 'sale', 'adjustment', 'transfer']
    if data['type'] not in valid_types:
        return jsonify({
            'error': 'Invalid transaction type',
            'valid_types': valid_types,
            'message': f'Transaction type must be one of: {", ".join(valid_types)}'
        }), 400
    
    # Validate quantity
    try:
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity format'}), 400
    
    # Validate unit cost if provided
    if data.get('unit_cost'):
        try:
            unit_cost = Decimal(str(data['unit_cost']))
            if unit_cost < 0:
                return jsonify({'error': 'Unit cost cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid unit cost format'}), 400
    
    return None