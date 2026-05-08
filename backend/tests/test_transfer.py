def test_successful_transfer_updates_balances(client):
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": 1,
            "to_account_id": 2,
            "amount": "250.00",
            "actor": "alice.test@example.com",
        },
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["message"] == "Transfer completed successfully"
    assert data["transaction"]["amount"] == "250.00"
    assert data["transaction"]["status"] == "completed"

    accounts_response = client.get("/api/accounts")
    accounts_data = accounts_response.get_json()

    account_1 = accounts_data["accounts"][0]
    account_2 = accounts_data["accounts"][1]

    assert account_1["balance"] == "4750.00"
    assert account_2["balance"] == "3450.00"


def test_transfer_creates_transaction_record(client):
    client.post(
        "/api/transfer",
        json={
            "from_account_id": 1,
            "to_account_id": 2,
            "amount": "100.00",
            "actor": "alice.test@example.com",
        },
    )

    response = client.get("/api/transactions")

    assert response.status_code == 200

    data = response.get_json()
    assert data["count"] == 1
    assert data["transactions"][0]["amount"] == "100.00"


def test_transfer_creates_audit_event(client):
    client.post(
        "/api/transfer",
        json={
            "from_account_id": 1,
            "to_account_id": 2,
            "amount": "100.00",
            "actor": "alice.test@example.com",
        },
    )

    response = client.get("/api/audit-events")

    assert response.status_code == 200

    data = response.get_json()
    assert data["count"] == 1
    assert data["audit_events"][0]["event_type"] == "transfer.completed"
    assert data["audit_events"][0]["outcome"] == "success"


def test_insufficient_balance_returns_error(client):
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": 1,
            "to_account_id": 2,
            "amount": "999999.00",
            "actor": "alice.test@example.com",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Insufficient balance"


def test_missing_transfer_fields_returns_error(client):
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": 1,
            "amount": "100.00",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Missing required fields"
    assert "to_account_id" in data["missing_fields"]


def test_transfer_to_same_account_returns_error(client):
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": 1,
            "to_account_id": 1,
            "amount": "100.00",
            "actor": "alice.test@example.com",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Source and destination accounts must be different"
