def register_and_login(client, email):
    client.post(
        "/api/auth/register", json={"email": email, "password": "Patient@12345"}
    )

    response = client.post(
        "/api/auth/login", data={"username": email, "password": "Patient@12345"}
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_unauthenticated_access(client):
    response = client.get("/api/appointments/")
    assert response.status_code == 401


def test_patient_can_create_appointment(client):
    headers = register_and_login(client, "appointment@example.com")

    response = client.post(
        "/api/appointments/",
        headers=headers,
        json={
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_time": "2027-01-15T10:00:00+05:30",
        },
    )

    assert response.status_code == 201


def test_patient_cannot_book_for_another_patient(client):
    headers = register_and_login(client, "owner@example.com")

    response = client.post(
        "/api/appointments/",
        headers=headers,
        json={
            "patient_id": 999,
            "doctor_id": 1,
            "appointment_time": "2027-01-16T10:00:00+05:30",
        },
    )

    assert response.status_code == 404
