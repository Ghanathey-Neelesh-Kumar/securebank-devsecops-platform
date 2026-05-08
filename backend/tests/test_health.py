def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "securebank-api"


def test_ready_endpoint(client):
    response = client.get("/ready")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "ready"
    assert data["service"] == "securebank-api"
