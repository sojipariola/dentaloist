# backend/app/seed/inventory_seeds.py
from app import db
from app.models import Product, ProductType, InventoryTransaction, InventoryTransactionType
import random
from datetime import datetime, timedelta

def seed_inventory_data():
    """Seed inventory products and transactions"""
    
    orgs = ["demo-dental-001", "smile-center-002"]
    product_types = ProductType.query.filter_by(is_active=True).all()
    transaction_types = InventoryTransactionType.query.filter_by(is_active=True).all()
    
    # Common dental products
    dental_products = [
        {"name": "Dental Anesthetic Cartridges", "sku": "ANES-001", "cost": 2.50},
        {"name": "Composite Resin", "sku": "COMP-001", "cost": 45.00},
        {"name": "Dental Floss", "sku": "FLOSS-001", "cost": 8.00},
        {"name": "Toothpaste", "sku": "PASTE-001", "cost": 12.00},
        {"name": "Dental Masks", "sku": "MASK-001", "cost": 15.00},
        {"name": "Gloves Medium", "sku": "GLOVE-M", "cost": 8.50},
        {"name": "X-Ray Film", "sku": "XRAY-001", "cost": 25.00},
        {"name": "Dental Bibs", "sku": "BIB-001", "cost": 12.00},
    ]
    
    products = []
    transactions = []
    
    for org_id in orgs:
        for product_data in dental_products:
            product_type = random.choice(product_types)
            
            product = Product(
                organization_id=org_id,
                name=product_data["name"],
                sku=product_data["sku"],
                product_type_id=product_type.id,
                description=f"Professional dental {product_data['name'].lower()}",
                cost_price=product_data["cost"],
                selling_price=round(product_data["cost"] * random.uniform(1.5, 2.5), 2),
                current_stock=random.randint(20, 100),
                min_stock_level=10,
                max_stock_level=200,
                is_active=True
            )
            products.append(product)
            
            # Create initial stock transaction
            purchase_type = InventoryTransactionType.query.filter_by(name="Purchase").first()
            
            transaction = InventoryTransaction(
                organization_id=org_id,
                product_id=product.id,
                transaction_type_id=purchase_type.id,
                quantity=product.current_stock,
                unit_cost=product.cost_price,
                total_cost=product.cost_price * product.current_stock,
                transaction_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                reference_number=f"PO-{random.randint(1000, 9999)}",
                notes="Initial stock purchase",
                created_by=1
            )
            transactions.append(transaction)
    
    db.session.bulk_save_objects(products)
    db.session.bulk_save_objects(transactions)
    db.session.commit()
    print(f"✅ {len(products)} products and {len(transactions)} inventory transactions seeded successfully.")