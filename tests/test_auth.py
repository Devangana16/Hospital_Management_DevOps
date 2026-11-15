
def test_register_patient(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newpatient@example.com",
            "password": "Patient@12345"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "newpatient@example.com"
    assert response.json()["role"] == "patient"


def test_duplicate_registration(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "Patient@12345"
    }

    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 409


def test_login(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "Patient@12345"
        }
    )

    response = client.post(
        "/api/auth/login",
        data={
            "username": "login@example.com",
            "password": "Patient@12345"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
