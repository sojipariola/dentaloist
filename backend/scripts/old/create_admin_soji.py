# backend/scripts/create_admin_soji.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Check if user exists
        user = User.query.filter_by(email='sojipariola@gmail.com').first()
        if user:
            # Update existing user
            user.password_hash = generate_password_hash('Soji1111')
            user.name = 'Soji Pariola'
            user.role = 'admin'
        else:
            # Create new user
            user = User(
                email='sojipariola@gmail.com',
                password_hash=generate_password_hash('Soji1111'),
                name='Soji Pariola',
                role='admin'
            )
            db.session.add(user)
        
        db.session.commit()
        print("Admin user created/updated successfully!")

if __name__ == '__main__':
    create_admin_user()
