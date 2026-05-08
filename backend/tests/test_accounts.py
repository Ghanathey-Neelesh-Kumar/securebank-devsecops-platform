def test_get_accounts(client):
    response = client.get("/api/accounts")

    assert response.status_code == 200

    data = response.get_json()
    assert data["count"] == 2
    assert data["accounts"][0]["account_number"] == "TEST-100001"
    assert data["accounts"][1]["account_number"] == "TEST-100002"


def test_get_single_account(client):
    response = client.get("/api/accounts/1")

    assert response.status_code == 200

    data = response.get_json()
    assert data["account_number"] == "TEST-100001"
    assert data["balance"] == "5000.00"


def test_get_missing_account_returns_404(client):
    response = client.get("/api/accounts/999")

    assert response.status_code == 404

    data = response.get_json()
    assert data["error"] == "Account not found"
