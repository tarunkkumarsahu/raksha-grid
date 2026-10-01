import pytest
from fastapi.testclient import TestClient

from app.config import allowed_hosts, cors_origins
from app.main import app


client = TestClient(app)


def test_health_and_readiness_are_available():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["version"] == app.version

    ready = client.get("/health/ready")
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"


def test_security_headers_and_request_id_are_present():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"


def test_development_configuration_has_safe_defaults():
    assert allowed_hosts()
    assert isinstance(cors_origins(), list)
