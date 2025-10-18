# backend/app/routes/roles.py
from flask import Blueprint, request, jsonify
from ..models import db
from ..models.models import Role
from ..utils.auth import token_required, admin_required
from ..utils.tenancy import tenant_required, multi_tenant_query

roles_bp = Blueprint("roles", __name__, url_prefix="/api/roles")


@roles_bp.route("", methods=["GET"])
@token_required
@admin_required
def list_roles():
    roles = Role.query.all()
    return jsonify({"roles": [r.to_dict() for r in roles]})


@roles_bp.route("/<int:role_id>", methods=["GET"])
@token_required
@admin_required
def get_role(role_id):
    role = Role.query.get_or_404(role_id)
    return jsonify({"role": role.to_dict()})


@roles_bp.route("", methods=["POST"])
@token_required
@admin_required
def create_role():
    data = request.get_json()
    role = Role(**data)
    db.session.add(role)
    db.session.commit()
    return jsonify({"role": role.to_dict()}), 201


@roles_bp.route("/<int:role_id>", methods=["PUT"])
@token_required
@admin_required
def update_role(role_id):
    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(role, key, value)
    db.session.commit()
    return jsonify({"role": role.to_dict()})


@roles_bp.route("/<int:role_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({"message": "Role deleted"})
