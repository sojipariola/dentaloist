# quick_sql_check.py
import sqlite3
import pandas as pd

def quick_data_check():
    db_path = '/home/soji/Documents/Projects/Dentaloist/backend/instance/dentaloist.db'
    conn = sqlite3.connect(db_path)
    
    print("📊 CURRENT DATA SNAPSHOT")
    print("=" * 60)
    
    # Sample data from key tables
    tables_to_check = [
        'organizations',
        'users', 
        'patients',
        'appointments',
        'invoices'
    ]
    
    for table in tables_to_check:
        print(f"\n{table.upper()}:")
        try:
            # Get sample data
            sample = pd.read_sql(f"SELECT * FROM {table} LIMIT 3;", conn)
            if len(sample) > 0:
                print(sample.to_string(index=False))
            else:
                print("  (No data)")
        except Exception as e:
            print(f"  Error: {e}")
    
    conn.close()

quick_data_check()
