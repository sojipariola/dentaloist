#!/usr/bin/env python3
"""Development DB inspector.

Run this from the repo root (or from backend/) to print the list of tables and row counts for a few key tables.
This uses your app factory so it respects the configured SQLALCHEMY_DATABASE_URI.
Intended for development only.
"""
from app import create_app
from app.extensions import db
from sqlalchemy import inspect

app = create_app()

def main():
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("Detected tables:", tables)

        # List of tables we commonly care about in this project
        interesting = [
            'users', 'organizations', 'patients', 'appointments',
            'treatments', 'inventory_items', 'inventory_alerts',
            'payments', 'financial_transactions', 'invoices',
            'notifications', 'oauth_clients', 'oauth_accounts',
        ]

        for t in interesting:
            if t in tables:
                try:
                    res = engine.execute(f"SELECT COUNT(*) FROM {t}")
                    count = res.scalar()
                except Exception as e:
                    count = f"error: {e}"
                print(f"  - {t}: {count}")
            else:
                print(f"  - {t}: (missing)")

        # Print column info for inventory_items if present
        if 'inventory_items' in tables:
            print("\ninventory_items columns:")
            cols = inspector.get_columns('inventory_items')
            for c in cols:
                print(f"  - {c['name']} : {c['type']}")

if __name__ == '__main__':
    main()