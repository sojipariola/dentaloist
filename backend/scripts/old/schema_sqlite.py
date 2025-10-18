import sqlite3

def print_sqlite_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=== SQLITE DATABASE SCHEMA ===")
    
    for table in tables:
        table_name = table[0]
        print(f"\n--- {table_name} ---")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for column in columns:
            col_id, name, type_, notnull, default, pk = column
            nullable = "NULL" if notnotnull else "NOT NULL"
            pk_flag = " PRIMARY KEY" if pk else ""
            default_str = f" DEFAULT {default}" if default else ""
            print(f"  {name:20} {type_:15} {nullable}{default_str}{pk_flag}")
    
    conn.close()

# Usage
print_sqlite_schema('dentaloist.db')