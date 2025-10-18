#!/usr/bin/env python3
import os
import sqlite3
from pathlib import Path

def reset_with_absolute_path():
    # Use absolute path to avoid any relative path issues
    base_dir = Path("/home/soji/Documents/Projects/Dentaloist/backend")
    db_path = base_dir / "instance" / "app.db"
    
    print(f"Using absolute path: {db_path}")
    
    # Ensure directory exists
    db_path.parent.mkdir(exist_ok=True)
    
    # Remove existing database
    if db_path.exists():
        db_path.unlink()
        print("🗑️ Removed existing database")
    
    # Create new database with SQLite
    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute("VACUUM")
        conn.close()
        print("✅ Database created with SQLite")
        
        # Verify
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()
        print(f"✅ SQLite version: {version[0]}")
        conn.close()
        
        # Set permissions
        db_path.chmod(0o644)
        print("✅ Database permissions set")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    reset_with_absolute_path()
