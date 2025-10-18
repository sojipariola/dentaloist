# backend/scripts/direct_sqlite_setup.py
import os
import sys
import sqlite3
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def direct_sqlite_setup():
    print("🔧 DIRECT SQLITE SETUP")
    print("=" * 50)
    
    db_path = 'instance/dentaloist.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Removed existing database")
    
    # Create new database with SQLite
    print("📦 Creating new database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Check if we can create tables
    try:
        # Try to create a simple appointments table
        cursor.execute("""
        CREATE TABLE appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            public_id TEXT UNIQUE NOT NULL,
            organization_id TEXT NOT NULL,
            patient_id INTEGER NOT NULL,
            dentist_id INTEGER NOT NULL,
            staff_id INTEGER NOT NULL,
            appointment_type_id INTEGER,
            status_id INTEGER,
            title TEXT,
            description TEXT,
            start_time DATETIME,
            end_time DATETIME,
            treatment_room TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (organization_id) REFERENCES organizations (public_id),
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (dentist_id) REFERENCES staff (id),
            FOREIGN KEY (staff_id) REFERENCES staff (id)
        )
        """)
        print("✅ appointments table created via direct SQL")
        
        # Create index
        cursor.execute("CREATE INDEX idx_appointments_org ON appointments (organization_id)")
        cursor.execute("CREATE INDEX idx_appointments_patient ON appointments (patient_id)")
        
        conn.commit()
        conn.close()
        
        # Now verify with SQLAlchemy
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'appointments' in tables:
                print("🎉 APPOINTMENTS TABLE VERIFIED WITH SQLALCHEMY!")
                return True
            else:
                print("❌ Table not visible to SQLAlchemy")
                return False
                
    except Exception as e:
        print(f"❌ Direct SQL failed: {e}")
        conn.close()
        return False

if __name__ == '__main__':
    success = direct_sqlite_setup()
    if success:
        print("\n✅ Direct setup successful!")
    else:
        print("\n❌ Direct setup failed!")
        sys.exit(1)