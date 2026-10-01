import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.database import SessionLocal
from app.main import app
from app.models import (
    AuditEventRecord,
    IncidentRecord,
    IncidentReportRecord,
    NotificationRecord,
    RefreshTokenRecord,
    UserRecord,
)
from app.services.demo_scenario import demo_scenario


client = TestClient(app)
PASSWORD = "StrongPass123!"
TEAM_CODE = "verified-team-code"


@pytest.fixture(autouse=True)
def clean_dashboard_data(monkeypatch):
    monkeypatch.setenv("RESPONSE_TEAM_REGISTRATION_CODE", TEAM_CODE)
    demo_scenario.reset()
    with SessionLocal.begin() as session:
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))
    yield
    demo_scenario.reset()
    with SessionLocal.begin() as session:
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))


def register_and_login(email: str, role: str):
    body = {
        "email": email,
        "display_name": "Dashboard Tester",
        "password": PASSWORD,
        "role": role,
    }
    if role == "response_team":
        body["response_team_verification_code"] = TEAM_CODE
    registered = client.post("/v1/auth/register", json=body)
    assert registered.status_code == 201
    logged_in = client.post(
        "/v1/auth/login",
        json={"email": email, "password": PASSWORD},
    )
    assert logged_in.status_code == 200
    return logged_in.json()["access_token"]


def auth(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_citizen_dashboard_is_frontend_ready_and_simulation_safe():
    token = register_and_login("citizen@example.com", "citizen")
    response = client.get("/v1/dashboard/citizen", headers=auth(token))

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "simulation"
    assert body["location"] == "Rampur"
    assert body["route"]["source"] == "simulation"
    assert body["route"]["destination_name"] == "Shelter A"
    assert body["shelters"]
    assert "Synthetic Bihar-style demo" in body["notice"]


def test_response_dashboard_requires_verified_response_team():
    citizen = register_and_login("citizen@example.com", "citizen")
    response = client.get("/v1/dashboard/response", headers=auth(citizen))
    assert response.status_code == 403

    team = register_and_login("team@example.com", "response_team")
    response = client.get("/v1/dashboard/response", headers=auth(team))
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "simulation"
    assert body["active_incidents"] == 0
    assert body["blocked_roads"] == []


def test_response_dashboard_reflects_verified_incident():
    citizen = register_and_login("citizen@example.com", "citizen")
    team = register_and_login("team@example.com", "response_team")

    reported = client.post(
        "/v1/incidents/reports",
        headers=auth(citizen),
        json={
            "category": "flood",
            "title": "Basantpur road flooded",
            "description": "Water has crossed the road and traffic cannot pass.",
            "severity": "high",
            "latitude": 25.0,
            "longitude": 86.0,
            "gps_verified": True,
            "independent_corroborations": 1,
        },
    )
    assert reported.status_code == 201
    incident_id = reported.json()["id"]
    report_id = reported.json()["reports"][0]["id"]

    reviewed = client.post(
        f"/v1/incidents/reports/{report_id}/review",
        headers=auth(team),
        json={"approve": True, "note": "Verified by response team."},
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["id"] == incident_id

    dashboard = client.get("/v1/dashboard/response", headers=auth(team))
    assert dashboard.status_code == 200
    body = dashboard.json()
    assert body["active_incidents"] == 1
    assert body["high_priority_incidents"] == 1
    assert body["priority_incidents"][0]["title"] == "Basantpur road flooded"

    citizen_dashboard = client.get("/v1/dashboard/citizen", headers=auth(citizen))
    assert citizen_dashboard.status_code == 200
    alerts = citizen_dashboard.json()["alerts"]
    assert any(alert["title"] == "Basantpur road flooded" for alert in alerts)
