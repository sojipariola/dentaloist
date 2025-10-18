# setup_database.py
import os
import sys

# Ensure project root is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
from app import create_app, db
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, CompileError, IntegrityError


def drop_duplicate_indexes_sqlite(db_path):
    """Drops duplicate indexes in SQLite if they exist."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
        indexes = [row[0] for row in cursor.fetchall()]
        for idx in indexes:
            if "idx_" in idx:  # Only drop custom app indexes
                cursor.execute(f"DROP INDEX IF EXISTS {idx};")
                print(f"⚙️  Dropped stale index: {idx}")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️  Could not drop duplicate indexes: {e}")

def clear_existing_lookup_data():
    """Clear existing lookup data to avoid duplicate conflicts"""
    try:
        from app.models import get_lookup_models
        lookup_models = get_lookup_models()
        
        for model in lookup_models:
            try:
                # Delete all records from the lookup table
                db.session.query(model).delete()
                print(f"🧹 Cleared existing data from {model.__name__}")
            except Exception as e:
                print(f"⚠️  Could not clear {model.__name__}: {e}")
                db.session.rollback()
        
        db.session.commit()
        print("✅ Cleared all existing lookup data")
    except Exception as e:
        print(f"⚠️  Error clearing lookup data: {e}")
        db.session.rollback()

def setup_database():
    app = create_app()

    with app.app_context():
        # --- Ensure instance directory ---
        instance_path = app.instance_path
        os.makedirs(instance_path, exist_ok=True)
        print(f"📁 Instance directory ready: {instance_path}")

        # --- Prepare database path ---
        db_path = os.path.join(instance_path, "dentaloist.db")
        is_sqlite = app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite")

        # --- Remove existing SQLite DB if necessary ---
        if is_sqlite and os.path.exists(db_path):
            os.remove(db_path)
            print(f"🧹 Removed old database file: {db_path}")

        # --- Drop duplicate indexes if SQLite ---
        if is_sqlite:
            drop_duplicate_indexes_sqlite(db_path)

        # --- Create all tables ---
        print("🧱 Creating database tables...")
        try:
            db.create_all()
            print("✅ All tables created successfully!")
        except (OperationalError, CompileError) as e:
            if "already exists" in str(e).lower():
                print("⚠️ Duplicate index detected — skipping creation.")
            else:
                raise

        # --- Clear existing lookup data first ---
        print("🧹 Clearing existing lookup data...")
        clear_existing_lookup_data()

        # --- Seed lookup data ---
        try:
            # Import here to ensure app context is properly set
            from scripts.migrate_enums_to_models import seed_lookup_data
            seed_lookup_data()
            print("🌱 Data seeded successfully!")
        except IntegrityError as e:
            print(f"❌ Integrity error during data seeding: {e}")
            db.session.rollback()
            # Try alternative approach
            print("🔄 Trying alternative seeding approach...")
            try:
                from scripts.migrate_enums_to_models import seed_lookup_data
                with db.session.no_autoflush:
                    seed_lookup_data()
                print("🌱 Data seeded successfully with no_autoflush!")
            except Exception as e2:
                print(f"❌ Alternative seeding also failed: {e2}")
        except Exception as e:
            print(f"❌ Error during data seeding: {e}")
            import traceback
            print(f"🔍 Detailed error: {traceback.format_exc()}")

        print("🎉 Database setup completed successfully!")

if __name__ == "__main__":
    setup_database()