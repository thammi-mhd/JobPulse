from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_jobs_endpoint():
    response = client.get("/api/v1/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "total_jobs" in data
    assert "jobs" in data
    assert isinstance(data["jobs"], list)

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "welcome to JobPulse"
    assert data["status"] == "success"

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "JobPulse is healthy and running"
    assert data["status"] == "success"

