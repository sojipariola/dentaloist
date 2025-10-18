# backend/tests/test_auth_tenancy.py
import json
from app import create_app, db
from app.models import User, Organization

def setup_module(module):
    app = create_app("testing")
    app.app_context().push()
    db.create_all()

def teardown_module(module):
    db.session.remove()
    db.drop_all()

def test_tenant_registration_and_login(client):
    client = create_app("testing").test_client()

    # Register tenant and user
    res = client.post("/api/auth/register", json={
        "email": "tenant@example.com",
        "password": "secure123",
        "organization_name": "TenantOrg"
    })
    assert res.status_code == 201
    data = res.get_json()
    tenant_id = data["tenant_id"]

    # Login with tenant header
    res = client.post("/api/auth/login",
        json={"email": "tenant@example.com", "password": "secure123"},
        headers={"X-Tenant-ID": str(tenant_id)}
    )
    assert res.status_code == 200
    assert res.get_json()["tenant_id"] == str(tenant_id)
