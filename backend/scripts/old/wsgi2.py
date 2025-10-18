from app import create_app, db
from app.models import Product

app = create_app()

def diagnose_product_issue():
    with app.app_context():
        print("🔍 Diagnosing Product-InventoryTransaction relationship...")
        
        # Check Product model
        product_inspector = db.inspect(Product)
        print(f"\n📦 Product relationships:")
        for rel in product_inspector.relationships:
            print(f"   - {rel.key}: {rel}")
        
        # Check if InventoryTransaction table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Database tables:")
        for table in sorted(tables):
            print(f"   - {table}")
        
        # Check if inventory_transactions table exists
        if 'inventory_transactions' in tables:
            print(f"\n✅ inventory_transactions table exists")
            # Check its columns
            columns = inspector.get_columns('inventory_transactions')
            print(f"   Columns in inventory_transactions:")
            for column in columns:
                fk_info = ""
                if column.get('foreign_keys'):
                    fk_info = f" [FK: {list(column['foreign_keys'])[0]}]"
                print(f"     - {column['name']}: {column['type']}{fk_info}")
        else:
            print(f"\n❌ inventory_transactions table does NOT exist")

diagnose_product_issue()