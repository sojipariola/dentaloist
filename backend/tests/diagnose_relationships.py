# tests/diagnose_relationships.py

from ..app import create_app, db

def diagnose_relationships():
    """Diagnose missing relationships in models"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        try:
            # Try to create all tables
            db.create_all()
            print("✅ All tables created successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n🔍 Let's check individual models...")
            
            # Check specific models
            from app.models import (
                User, Organization, AnalyticsDashboard, AnalyticsWidget, Widget
            )
            
            models_to_check = [
                ('User', User),
                ('Organization', Organization),
                ('AnalyticsDashboard', AnalyticsDashboard),
                ('AnalyticsWidget', AnalyticsWidget),
                ('Widget', Widget)
            ]
            
            for name, model in models_to_check:
                try:
                    model.__table__.create(db.engine)
                    print(f"✅ {name} table created successfully")
                    model.__table__.drop(db.engine)
                except Exception as e:
                    print(f"❌ {name} failed: {e}")

if __name__ == '__main__':
    diagnose_relationships()