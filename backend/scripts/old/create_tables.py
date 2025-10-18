# create_tables.py
from .app import create_app, db
from .app.models.appointment import AppointmentStatus
# Import other models as needed

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("All tables created successfully!")
    
    # Now run your data migration
    from scripts.migrate_enums_to_models import seed_lookup_data
    seed_lookup_data()
    print("Data seeded successfully!")
