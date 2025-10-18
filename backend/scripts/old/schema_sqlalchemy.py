import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from sqlalchemy import inspect

def create_app():
    # Adjust this based on your actual app factory
    from app import create_app
    return create_app()

def print_database_schema():
    app = create_app()
    
    with app.app_context():
        from app.models import db
        
        inspector = inspect(db.engine)
        
        # Open file for writing
        with open('scripts/schema_sqlalchemy.txt', 'w') as f:
            # Write to both console and file
            def write_output(text):
                print(text, end='')
                f.write(text)
            
            write_output("=== DATABASE SCHEMA ===\n")
            
            for table_name in inspector.get_table_names():
                write_output(f"\n--- {table_name} ---\n")
                
                columns = inspector.get_columns(table_name)
                for column in columns:
                    nullable = "NULL" if column['nullable'] else "NOT NULL"
                    default = f" DEFAULT {column['default']}" if column['default'] else ""
                    write_output(f"  {column['name']:25} {str(column['type']):30} {nullable}{default}\n")
                
                # Primary keys
                pk = inspector.get_pk_constraint(table_name)
                if pk['constrained_columns']:
                    write_output(f"  PK: {', '.join(pk['constrained_columns'])}\n")
                
                # Foreign keys
                fks = inspector.get_foreign_keys(table_name)
                for fk in fks:
                    write_output(f"  FK: {', '.join(fk['constrained_columns'])} -> {fk['referred_table']}({', '.join(fk['referred_columns'])})\n")
        
        print("\nDatabase schema saved to scripts/schema_sqlalchemy.txt")

if __name__ == "__main__":
    print_database_schema()