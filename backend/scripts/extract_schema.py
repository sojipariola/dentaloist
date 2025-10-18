#!/usr/bin/env python3
"""
Extract database schema for proper seeding
"""

import sqlite3
import json
from pathlib import Path

def extract_schema():
    """Extract complete database schema"""
    db_path = Path('instance/dentaloist.db')
    
    if not db_path.exists():
        print("❌ Database not found")
        return None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📊 EXTRACTING DATABASE SCHEMA")
    print("=" * 50)
    
    schema = {}
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall() if not row[0].startswith('sqlite_')]
    
    print(f"📋 Found {len(tables)} tables:")
    
    for table in sorted(tables):
        print(f"\n🏷️  Table: {table}")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        schema[table] = {
            'columns': [],
            'constraints': [],
            'foreign_keys': []
        }
        
        print("   Columns:")
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            schema[table]['columns'].append({
                'name': col_name,
                'type': col_type,
                'not_null': bool(not_null),
                'default': default_val,
                'primary_key': bool(pk)
            })
            print(f"     - {col_name} ({col_type}) {'PK' if pk else ''} {'NOT NULL' if not_null else ''}")
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        foreign_keys = cursor.fetchall()
        
        for fk in foreign_keys:
            schema[table]['foreign_keys'].append({
                'from_column': fk[3],
                'to_table': fk[2],
                'to_column': fk[4]
            })
    
    conn.close()
    
    # Save schema to file
    schema_file = Path('database_schema.json')
    with open(schema_file, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print(f"\n💾 Schema saved to: {schema_file}")
    return schema

def analyze_required_fields(schema):
    """Analyze which fields are required for each table"""
    print("\n🔍 ANALYZING REQUIRED FIELDS")
    print("=" * 40)
    
    required_fields = {}
    
    for table, table_info in schema.items():
        required_fields[table] = []
        for column in table_info['columns']:
            if column['not_null'] and not column['primary_key'] and column['default'] is None:
                required_fields[table].append(column['name'])
        
        if required_fields[table]:
            print(f"📋 {table}: {', '.join(required_fields[table])}")
    
    return required_fields

if __name__ == '__main__':
    schema = extract_schema()
    if schema:
        analyze_required_fields(schema)