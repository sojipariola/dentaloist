# routes/users.py
# backend/app/routes/users.py

from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..models import db, User
from ..utils.tenancy import tenant_required
from ..utils.auth import get_current_user, permission_required

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


# ===== Create User (Admin only) =====
@users_bp.route("/", methods=["POST"])
@jwt_required()
@tenant_required
@permission_required(["ORG_ADMIN", "SUPER_ADMIN"])
def create_user():
    data = request.get_json() or {}
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        phone=data.get("phone"),
        role=data.get("role", "USER"),  # Default role
        organization_id=data.get("organization_id", g.current_tenant),
        specialization=data.get("specialization"),
        license_number=data.get("license_number"),
        is_admin=data.get("is_admin", False),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": user.to_dict()}), 201


# ===== Get Current User Profile =====
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user = get_current_user()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify({"user": user.to_dict()})


# ===== Update Profile (self only) =====
@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    user = get_current_user()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
        
    data = request.get_json() or {}

    # Only allow updating certain fields for self
    allowed_fields = [
        "first_name", "last_name", "phone", "bio", "date_of_birth", 
        "gender", "address", "emergency_contact", "specialization", 
        "license_number", "experience_years"
    ]
    
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"user": user.to_dict()})


# ===== List Users (Tenant scoped) =====
@users_bp.route("/", methods=["GET"])
@jwt_required()
@tenant_required
@permission_required(["ORG_ADMIN", "SUPER_ADMIN"])
def list_users():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    search = request.args.get("search")

    query = User.query.filter_by(organization_id=g.current_tenant)

    if search:
        query = query.filter(
            (User.email.ilike(f"%{search}%")) |
            (User.first_name.ilike(f"%{search}%")) |
            (User.last_name.ilike(f"%{search}%"))
        )

    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()

    return jsonify({
        "users": [u.to_dict() for u in users],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
    })


# ===== Update Settings =====
@users_bp.route("/me/settings", methods=["PUT"])
@jwt_required()
def update_settings():
    user = get_current_user()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
        
    data = request.get_json() or {}

    # Initialize settings if not exists
    if user.settings is None:
        user.settings = {}
    
    # Merge into existing JSON
    user.settings.update(data)
    user.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"settings": user.settings}), 200


# ===== Get Settings =====
@users_bp.route("/me/settings", methods=["GET"])
@jwt_required()
def get_settings():
    user = get_current_user()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
        
    # Return empty dict if settings is None
    settings = user.settings if user.settings else {}
    return jsonify({"settings": settings}), 200


# ===== Get Profile by ID (self only) =====
@users_bp.route("/<int:user_id>/profile", methods=["GET"])
@jwt_required()
def get_profile(user_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"message": "Unauthorized"}), 401
        
    # Users can only view their own profile via this endpoint
    if current_user.id != user_id:
        return jsonify({"message": "Forbidden"}), 403

    return jsonify({"user": current_user.to_dict()}), 200


# ===== Change Password (self only) =====
@users_bp.route("/me/password", methods=["PUT"])
@jwt_required()
def change_password():
    user = get_current_user()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
        
    data = request.get_json() or {}

    if not data.get("old_password") or not data.get("new_password"):
        return jsonify({"message": "Old and new passwords required"}), 400

    if not check_password_hash(user.password_hash, data["old_password"]):
        return jsonify({"message": "Old password is incorrect"}), 400

    user.password_hash = generate_password_hash(data["new_password"])
    user.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200   


# ===== Delete User (Admin only) =====
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@tenant_required
@permission_required(["ORG_ADMIN", "SUPER_ADMIN"])
def delete_user(user_id):
    # Prevent self-deletion
    current_user = get_current_user()
    if current_user.id == user_id:
        return jsonify({"message": "Cannot delete your own account"}), 400
        
    user = User.query.filter_by(id=user_id, organization_id=g.current_tenant).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


# ===== Get User by ID (Admin only) =====
@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@tenant_required
@permission_required(["ORG_ADMIN", "SUPER_ADMIN"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id, organization_id=g.current_tenant).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200


# ===== Update User by ID (Admin only) =====
@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@tenant_required
@permission_required(["ORG_ADMIN", "SUPER_ADMIN"])
def update_user(user_id):
    user = User.query.filter_by(id=user_id, organization_id=g.current_tenant).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json() or {}

    # Admin can update more fields than regular users
    updatable_fields = [
        "first_name", "last_name", "phone", "bio", "date_of_birth", 
        "gender", "address", "emergency_contact", "specialization", 
        "license_number", "experience_years", "is_active", "role"
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(user, field, data[field])
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"user": user.to_dict()}), 200