def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_register_and_login(client):
    resp = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@example.com"

    resp = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "testpass123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_create_and_list_jobs(client):
    client.post("/auth/register", json={
        "email": "jobuser@example.com",
        "password": "testpass123",
        "full_name": "Job User",
    })
    token = client.post("/auth/login", data={
        "username": "jobuser@example.com",
        "password": "testpass123",
    }).json()["access_token"]

    resp = client.post("/jobs/", json={
        "title": "Software Engineer",
        "description": "Build ML systems.",
        "location": "Remote",
    })
    assert resp.status_code == 200
    assert resp.json()["title"] == "Software Engineer"

    resp = client.get("/jobs/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_predict_structured(client):
    resp = client.post("/predict/structured", json={
        "title": "Work from home - earn $5000 weekly",
        "description": "No experience needed. Send money for training.",
        "requirements": "Bank account and SSN required.",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "is_fraudulent" in data
    assert "confidence_score" in data
    assert "risk_percentage" in data
    assert "suspicious_phrases" in data
