def test_health_endpoint(client):
    """Simple health endpoint test"""
    response = client.get("/api/auth/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "auth"
