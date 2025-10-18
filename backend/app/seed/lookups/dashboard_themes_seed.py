# app/seed/lookups/dashboard_themes_seed.py

from app import db
from app.models import DashboardTheme
import uuid


def seed_dashboard_themes():
    """Seed dashboard themes with required code field"""
    
    themes_data = [
        {
            'name': 'Light',
            'code': 'LIGHT',
            'description': 'Clean light theme with white background',
            'css_class': 'theme-light',
            'primary_color': '#3498db',
            'secondary_color': '#2c3e50',
            'is_dark': False,
            'sort_order': 0,
            'is_active': True
        },
        {
            'name': 'Dark', 
            'code': 'DARK',
            'description': 'Modern dark theme for reduced eye strain',
            'css_class': 'theme-dark',
            'primary_color': '#3498db',
            'secondary_color': '#ecf0f1',
            'is_dark': True,
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Blue',
            'code': 'BLUE',
            'description': 'Professional blue color scheme',
            'css_class': 'theme-blue',
            'primary_color': '#2980b9',
            'secondary_color': '#34495e',
            'is_dark': False,
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Green',
            'code': 'GREEN',
            'description': 'Calming green theme for healthcare',
            'css_class': 'theme-green',
            'primary_color': '#27ae60',
            'secondary_color': '#2c3e50',
            'is_dark': False,
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'High Contrast',
            'code': 'HIGH_CONTRAST',
            'description': 'High contrast theme for accessibility',
            'css_class': 'theme-high-contrast',
            'primary_color': '#000000',
            'secondary_color': '#ffffff',
            'is_dark': False,
            'sort_order': 4,
            'is_active': True
        },
        {
            'name': 'Warm',
            'code': 'WARM',
            'description': 'Warm color palette with orange tones',
            'css_class': 'theme-warm',
            'primary_color': '#e67e22',
            'secondary_color': '#d35400',
            'is_dark': False,
            'sort_order': 5,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for theme_data in themes_data:
            # Check if theme already exists by code
            existing_theme = DashboardTheme.query.filter_by(code=theme_data['code']).first()
            
            if existing_theme:
                # Update existing theme
                print(f"🔄 Updating existing dashboard theme: {theme_data['name']}")
                for key, value in theme_data.items():
                    setattr(existing_theme, key, value)
                updated_count += 1
            else:
                # Add new theme
                print(f"✅ Adding new dashboard theme: {theme_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in theme_data:
                    theme_data['public_id'] = str(uuid.uuid4())
                
                theme = DashboardTheme(**theme_data)
                db.session.add(theme)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Dashboard Themes seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("🎨 Dashboard Themes added:")
            for theme_data in themes_data:
                theme = DashboardTheme.query.filter_by(code=theme_data['code']).first()
                if theme:
                    mode = "Dark" if theme.is_dark else "Light"
                    print(f"   • {theme.name} - {mode} mode - Primary: {theme.primary_color}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding dashboard themes: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_dashboard_themes()