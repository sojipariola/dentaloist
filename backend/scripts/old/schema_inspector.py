from sqlalchemy import create_engine, inspect

# Create engine (replace with your database URL)
engine = create_engine('sqlite:///dentaloist.db')  # or your actual DB URL

# Create inspector
inspector = inspect(engine)

# Get all table names
table_names = inspector.get_table_names()
print("=== DATABASE SCHEMA ===")
print(f"Tables: {table_names}\n")

# Print schema for each table
for table_name in table_names:
    print(f"--- Table: {table_name} ---")
    
    # Get columns
    columns = inspector.get_columns(table_name)
    for column in columns:
        nullable = "NULL" if column['nullable'] else "NOT NULL"
        default = f" DEFAULT {column['default']}" if column['default'] else ""
        print(f"  {column['name']:20} {column['type']} {nullable}{default}")
    
    # Get primary keys
    pk = inspector.get_pk_constraint(table_name)
    if pk['constrained_columns']:
        print(f"  Primary Key: {pk['constrained_columns']}")
    
    # Get foreign keys
    fks = inspector.get_foreign_keys(table_name)
    for fk in fks:
        print(f"  Foreign Key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    
    print()