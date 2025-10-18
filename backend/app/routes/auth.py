# backend/app/routes/auth.py
from flask import Blueprint, request, jsonify, current_app, g
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app.models import User, Organization, db
from app.utils.tenancy import get_current_tenant_id
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user under a tenant (organization)."""
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    organization_name = data.get("organization_name")

    if not all([email, password, organization_name]):
        return jsonify({"message": "Missing required fields"}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    # Create new tenant organization
    organization = Organization(name=organization_name)
    db.session.add(organization)
    db.session.flush()  # Get org ID before commit

    # Create user
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        organization_id=organization.id,
        role="OWNER"
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message": "Registration successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "tenant_id": organization.id
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Tenant-aware login."""
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    tenant_header = request.headers.get("X-Tenant-ID")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Tenant enforcement
    if tenant_header:
        if str(user.organization_id) != str(tenant_header):
            return jsonify({"message": "Tenant mismatch"}), 403
        g.tenant_id = tenant_header
    else:
        g.tenant_id = str(user.organization_id)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "tenant_id": g.tenant_id
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """Get current user info and tenant context."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": str(user.id),
        "email": user.email,
        "role": user.role,
        "organization_id": str(user.organization_id),
        "tenant_id": get_current_tenant_id()
    })


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh JWT tokens."""
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_access_token})
