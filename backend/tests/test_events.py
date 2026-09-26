import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.database import SessionLocal
from app.main import app
from app.models import (
    AuditEventRecord,
    IncidentRecord,
    IncidentReportRecord,
    IncidentRoadLinkRecord,
    NetworkMeta,
    NotificationRecord,
    RefreshTokenRecord,
    RoadEdgeRecord,
    RoadNodeRecord,
    UserRecord,
)


client = TestClient(app)
PASSWORD = "StrongPass123!"
TEAM_CODE = "verified-team-code"


@pytest.fixture(autouse=True)
def clean_tables(monkeypatch):
    monkeypatch.setenv("RESPONSE_TEAM_REGISTRATION_CODE", TEAM_CODE)
    with SessionLocal.begin() as session:
        for model in (
            NotificationRecord,
            IncidentRoadLinkRecord,
            AuditEventRecord,
            IncidentReportRecord,
            IncidentRecord,
            RoadEdgeRecord,
            RoadNodeRecord,
            NetworkMeta,
            RefreshTokenRecord,
            UserRecord,
        ):
            session.execute(delete(model))
    yield
    with SessionLocal.begin() as session:
        for model in (
            NotificationRecord,
            IncidentRoadLinkRecord,
            AuditEventRecord,
            IncidentReportRecord,
            IncidentRecord,
            RoadEdgeRecord,
            RoadNodeRecord,
            NetworkMeta,
            RefreshTokenRecord,
            UserRecord,
        ):
            session.execute(delete(model))


def auth(token: str):
    return {"Authorization": f"Bearer {token}"}


def register_and_login(email: str, role: str, verified: bool = True):
    body = {"email": email, "display_name": "Test User", "password": PASSWORD, "role": role}
    if role == "response_team" and verified:
        body["response_team_verification_code"] = TEAM_CODE
    assert client.post("/v1/auth/register", json=body).status_code == 201
    login = client.post("/v1/auth/login", json={"email": email, "password": PASSWORD})
    assert login.status_code == 200
    return login.json()["access_token"]


def incident_payload():
    return {
        "category": "flood",
        "title": "Flooded lane near Rampur",
        "description": "Water is crossing the local road.",
        "severity": "high",
        "latitude": 26.12,
        "longitude": 86.60,
        "photo_reference": "demo/flood.jpg",
        "gps_verified": True,
        "independent_corroborations": 2,
        "contradicting_reports": 0,
    }


def test_verified_incident_emits_notifications_and_events():
    team = register_and_login("team@example.com", "response_team")
    citizen = register_and_login("citizen@example.com", "citizen")

    created = client.post(
        "/v1/incidents/reports",
        json=incident_payload(),
        headers=auth(team),
    )
    assert created.status_code == 201
    incident_id = created.json()["id"]

    response_notifications = client.get("/v1/notifications", headers=auth(citizen))
    assert response_notifications.status_code == 200
    items = response_notifications.json()["items"]
    assert any(item["event_type"] == "incident.verified" for item in items)

    events = client.get("/v1/events", headers=auth(team))
    assert events.status_code == 200
    assert any(item["action"] == "incident_report_submitted" for item in events.json()["items"])

    notification_id = items[0]["id"]
    marked = client.patch(
        f"/v1/notifications/{notification_id}",
        json={"read": True},
        headers=auth(citizen),
    )
    assert marked.status_code == 200
    assert marked.json()["read_at"] is not None

    assert incident_id > 0


def test_notification_visibility_is_role_aware():
    citizen = register_and_login("citizen@example.com", "citizen")
    team = register_and_login("team@example.com", "response_team")

    response = client.get("/v1/notifications", headers=auth(citizen))
    assert response.status_code == 200
    assert response.json()["items"] == []

    response = client.get("/v1/notifications", headers=auth(team))
    assert response.status_code == 200
    assert response.json()["items"] == []
