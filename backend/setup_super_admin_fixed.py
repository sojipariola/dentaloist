import os
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import User, Organization, UserRole
from werkzeug.security import generate_password_hash

def setup_super_admin():
    app = create_app()
    
    with app.app_context():
        print("👑 Setting up Super Admin account...")
        
        # Check if super admin role exists
        super_admin_role = UserRole.query.filter_by(code='SUPER_ADMIN').first()
        if not super_admin_role:
            print("❌ SUPER_ADMIN role not found! Please seed user roles first.")
            return
        
        # Check if user already exists
        existing_user = User.query.filter_by(email='sojipariola@gmail.com').first()
        
        if existing_user:
            print("✅ Super admin user already exists:")
            print(f"   Name: {existing_user.first_name} {existing_user.last_name}")
            print(f"   Email: {existing_user.email}")
            print(f"   Organization: {existing_user.organization_id}")
            
            # Update password
            existing_user.password_hash = generate_password_hash('Soji1111')
            
            # Safe role assignment
            try:
                if super_admin_role not in existing_user.roles:
                    existing_user.roles.append(super_admin_role)
                    print("   Added SUPER_ADMIN role")
            except Exception as e:
                print(f"   ⚠️  Could not add role directly: {e}")
                # Alternative approach
                self._assign_role_safely(existing_user, super_admin_role)
            
            db.session.commit()
            print("✅ Password updated and role verified")
            
        else:
            # Create new super admin user
            print("🆕 Creating new super admin user...")
            
            # Get first organization or create a dummy one for super admin
            first_org = Organization.query.first()
            if not first_org:
                print("❌ No organizations found! Please seed organizations first.")
                return
            
            super_admin = User(
                first_name='Soji',
                last_name='Pariola',
                email='sojipariola@gmail.com',
                password_hash=generate_password_hash('Soji1111'),
                organization_id=first_org.public_id,
                public_id='super_admin_soji',
                is_active=True,
                email_verified=True
            )
            
            db.session.add(super_admin)
            db.session.flush()  # Get the ID without committing
            
            # Safe role assignment
            try:
                super_admin.roles.append(super_admin_role)
                print("   Added SUPER_ADMIN role via relationship")
            except Exception as e:
                print(f"   ⚠️  Could not add role via relationship: {e}")
                # Use alternative method
                self._assign_role_using_association(super_admin, super_admin_role)
            
            db.session.commit()
            
            print("✅ Super admin created successfully!")
            print(f"   Name: Soji Pariola")
            print(f"   Email: sojipariola@gmail.com")
            print(f"   Password: Soji1111")
            print(f"   Organization: {first_org.name}")
        
        # Verify setup
        print("\n🔍 Verification:")
        user = User.query.filter_by(email='sojipariola@gmail.com').first()
        if user:
            try:
                roles = [role.name for role in user.roles]
                print(f"   Roles: {roles}")
                print(f"   Is Super Admin: {'SUPER_ADMIN' in roles}")
            except Exception as e:
                print(f"   ⚠️  Could not fetch roles: {e}")
                # Check via association table
                self._check_roles_alternative(user)

def _assign_role_safely(self, user, role):
    """Alternative method to assign role if relationship doesn't work"""
    try:
        # If there's a direct association table
        from app.models import user_roles  # Adjust based on your association table name
        
        stmt = user_roles.insert().values(
            user_id=user.id,
            role_id=role.id
        )
        db.session.execute(stmt)
        print("   ✅ Role assigned via association table")
    except Exception as e:
        print(f"   ❌ Could not assign role via association: {e}")

def _assign_role_using_association(self, user, role):
    """Another alternative using raw SQL if needed"""
    try:
        # Direct SQL insertion into association table
        # Adjust table and column names based on your schema
        sql = """
        INSERT INTO user_roles_association (user_id, role_id) 
        VALUES (:user_id, :role_id)
        """
        db.session.execute(sql, {'user_id': user.id, 'role_id': role.id})
        print("   ✅ Role assigned via direct SQL")
    except Exception as e:
        print(f"   ❌ Could not assign role via SQL: {e}")

def _check_roles_alternative(self, user):
    """Alternative method to check user roles"""
    try:
        # Direct query to association table
        from app.models import UserRole
        
        sql = """
        SELECT r.name 
        FROM user_roles r 
        JOIN user_roles_association ura ON r.id = ura.role_id 
        WHERE ura.user_id = :user_id
        """
        result = db.session.execute(sql, {'user_id': user.id})
        roles = [row[0] for row in result]
        print(f"   Roles (alternative check): {roles}")
    except Exception as e:
        print(f"   ❌ Could not check roles alternatively: {e}")

if __name__ == '__main__':
    setup_super_admin()
