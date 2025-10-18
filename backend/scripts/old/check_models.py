# check_models.py
from app import create_app, db

app = create_app()

with app.app_context():
    # Check if models are loaded
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    
    # Print metadata info
    print("Metadata tables:")
    for table in db.metadata.tables:
        print(f"  - {table}")
    
    print(f"Total tables in metadata: {len(db.metadata.tables)}")
