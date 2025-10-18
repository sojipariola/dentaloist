# check_instance.py
import os
import sqlite3
from pathlib import Path

def check_instance_folder():
    """Check the instance folder contents"""
    backend_path = Path('/home/soji/Documents/Projects/Dentaloist/backend')
    instance_path = backend_path / 'instance'
    
    print("🔍 Checking instance folder...")
    
    # Check if instance folder exists
    if not instance_path.exists():
        print("❌ Instance folder does not exist")
        print("📁 Current directory contents:")
        for item in backend_path.iterdir():
            print(f"   - {item.name} ({'dir' if item.is_dir() else 'file'})")
        return
    
    print(f"✅ Instance folder found: {instance_path}")
    print("📁 Instance folder contents:")
    
    for item in instance_path.iterdir():
        item_type = 'dir' if item.is_dir() else 'file'
        size = item.stat().st_size if item.is_file() else 0
        print(f"   - {item.name} ({item_type}, {size} bytes)")
        
        # If it's a SQLite database, show some info
        if item.suffix in ['.db', '.sqlite', '.sqlite3']:
            check_sqlite_database(item)

def check_sqlite_database(db_path):
    """Check SQLite database contents"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"   📊 Database: {db_path.name}")
        print(f"   📋 Tables: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            # Count rows in each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"      - {table_name}: {count} rows")
            
        conn.close()
    except Exception as e:
        print(f"   ❌ Error reading database: {e}")

def check_config_files():
    """Check for configuration files"""
    backend_path = Path('/home/soji/Documents/Projects/Dentaloist/backend')
    config_files = [
        backend_path / 'instance' / 'config.py',
        backend_path / 'config.py',
        backend_path / '.env',
        backend_path / '.flaskenv'
    ]
    
    print("\n🔧 Checking configuration files:")
    for config_file in config_files:
        if config_file.exists():
            print(f"   ✅ {config_file.name} exists")
            if config_file.is_file():
                try:
                    content = config_file.read_text()
                    print(f"      Size: {len(content)} bytes")
                    # Show first few lines
                    lines = content.split('\n')[:5]
                    for line in lines:
                        if line.strip() and not line.strip().startswith('#'):
                            print(f"      Sample: {line.strip()[:50]}...")
                            break
                except Exception as e:
                    print(f"      Error reading: {e}")
        else:
            print(f"   ❌ {config_file.name} not found")

if __name__ == "__main__":
    check_instance_folder()
    check_config_files()
