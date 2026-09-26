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


client = TestClient(app)
PASSWORD = "StrongPass123!"
TEAM_CODE = "verified-team-code"


@pytest.fixture(autouse=True)
def clean_tables(monkeypatch):
    monkeypatch.setenv("RESPONSE_TEAM_REGISTRATION_CODE", TEAM_CODE)
    with SessionLocal.begin() as session:
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))
    yield
    with SessionLocal.begin() as session:
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))


def register_and_login(email: str, role: str = "citizen", verified_team: bool = True):
    body = {
        "email": email,
        "display_name": "Test User",
        "password": PASSWORD,
        "role": role,
    }
    if role == "response_team" and verified_team:
        body["response_team_verification_code"] = TEAM_CODE

    registered = client.post("/v1/auth/register", json=body)
    assert registered.status_code == 201
    login = client.post(
        "/v1/auth/login",
        json={"email": email, "password": PASSWORD},
    )
    assert login.status_code == 200
    return registered.json(), login.json()["access_token"]


def auth(token: str):
    return {"Authorization": f"Bearer {token}"}


def incident_payload():
    return {
        "category": "flood",
        "title": "Water crossing local road",
        "description": "Water is rising across the road near the bridge.",
        "severity": "high",
        "latitude": 25.61,
        "longitude": 85.14,
        "photo_reference": None,
        "gps_verified": True,
        "independent_corroborations": 2,
        "contradicting_reports": 0,
    }


def response_team_payload():
    payload = incident_payload()
    payload.update(
        {
            "title": "Response team confirms road flooding",
            "photo_reference": "evidence/demo-photo-001",
        }
    )
    return payload


def test_incident_routes_require_authentication():
    response = client.post("/v1/incidents/reports", json=incident_payload())
    assert response.status_code == 401


def test_citizen_report_enters_pending_verification():
    user, token = register_and_login("citizen@example.com")
    response = client.post(
        "/v1/incidents/reports",
        json=incident_payload(),
        headers=auth(token),
    )
    assert response.status_code == 201
    body = response.json()

    assert body["status"] == "reported"
    assert body["verification_status"] == "pending"
    assert body["source_type"] == "citizen"
    assert body["report_count"] == 1
    assert body["reports"][0]["reporter_user_id"] == user["id"]
    assert body["reports"][0]["reporter_role"] == "citizen"
    assert body["reports"][0]["verification_status"] == "pending"
    assert body["audit_events"][0]["actor_user_id"] == user["id"]


def test_verified_response_team_report_becomes_active():
    user, token = register_and_login("team@example.com", role="response_team")
    response = client.post(
        "/v1/incidents/reports",
        json=response_team_payload(),
        headers=auth(token),
    )
    assert response.status_code == 201
    body = response.json()

    assert user["is_verified"] is True
    assert body["status"] == "active"
    assert body["verification_status"] == "verified"
    assert body["source_type"] == "response_team"
    assert body["reports"][0]["confidence"] >= 0.75


def test_unverified_response_team_report_does_not_auto_verify():
    user, token = register_and_login(
        "pending-team@example.com",
        role="response_team",
        verified_team=False,
    )
    response = client.post(
        "/v1/incidents/reports",
        json=response_team_payload(),
        headers=auth(token),
    )
    assert response.status_code == 201
    body = response.json()

    assert user["is_verified"] is False
    assert body["status"] == "reported"
    assert body["verification_status"] == "pending"


def test_verified_response_team_can_approve_then_resolve():
    _, citizen_token = register_and_login("citizen@example.com")
    team_user, team_token = register_and_login("team@example.com", role="response_team")

    created = client.post(
        "/v1/incidents/reports",
        json=incident_payload(),
        headers=auth(citizen_token),
    ).json()
    report_id = created["reports"][0]["id"]
    incident_id = created["id"]

    reviewed = client.post(
        f"/v1/incidents/reports/{report_id}/review",
        json={"approve": True, "note": "Field team confirmed water over road."},
        headers=auth(team_token),
    )
    assert reviewed.status_code == 200
    reviewed_body = reviewed.json()
    assert reviewed_body["status"] == "active"
    assert reviewed_body["verification_status"] == "verified"
    assert reviewed_body["reports"][0]["reviewed_by"] == team_user["email"]

    resolved = client.post(
        f"/v1/incidents/{incident_id}/resolve",
        json={"note": "Water receded and road inspected."},
        headers=auth(team_token),
    )
    assert resolved.status_code == 200
    body = resolved.json()
    assert body["status"] == "resolved"
    assert body["resolved_at"] is not None
    actions = [event["action"] for event in body["audit_events"]]
    assert actions == [
        "incident_report_submitted",
        "incident_report_approved",
        "incident_resolved",
    ]


def test_citizen_cannot_review_incident_reports():
    _, first_citizen = register_and_login("reporter@example.com")
    _, second_citizen = register_and_login("reviewer@example.com")
    created = client.post(
        "/v1/incidents/reports",
        json=incident_payload(),
        headers=auth(first_citizen),
    ).json()

    response = client.post(
        f"/v1/incidents/reports/{created['reports'][0]['id']}/review",
        json={"approve": True},
        headers=auth(second_citizen),
    )
    assert response.status_code == 403


def test_pending_report_can_be_rejected_by_response_team():
    _, citizen_token = register_and_login("citizen@example.com")
    _, team_token = register_and_login("team@example.com", role="response_team")
    created = client.post(
        "/v1/incidents/reports",
        json=incident_payload(),
        headers=auth(citizen_token),
    ).json()

    response = client.post(
        f"/v1/incidents/reports/{created['reports'][0]['id']}/review",
        json={"approve": False, "note": "Team found the road clear."},
        headers=auth(team_token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "rejected"
    assert body["verification_status"] == "rejected"


def test_pending_incident_cannot_be_resolved():
    _, citizen_token = register_and_login("citizen@example.com")
    _, team_token = register_and_login("team@example.com", role="response_team")
    created = client.post(
        "/v1/incidents/reports",
        json=incident_payload(),
        headers=auth(citizen_token),
    ).json()

    response = client.post(
        f"/v1/incidents/{created['id']}/resolve",
        json={"note": "Invalid transition attempt"},
        headers=auth(team_token),
    )
    assert response.status_code == 409


def test_list_can_filter_by_status_for_authenticated_user():
    _, citizen_token = register_and_login("citizen@example.com")
    _, team_token = register_and_login("team@example.com", role="response_team")

    client.post(
        "/v1/incidents/reports",
        json=incident_payload(),
        headers=auth(citizen_token),
    )
    client.post(
        "/v1/incidents/reports",
        json=response_team_payload(),
        headers=auth(team_token),
    )

    active = client.get("/v1/incidents?status=active", headers=auth(citizen_token))
    assert active.status_code == 200
    data = active.json()
    assert len(data) == 1
    assert data[0]["status"] == "active"


def test_missing_incident_returns_404_for_authenticated_user():
    _, token = register_and_login("citizen@example.com")
    response = client.get("/v1/incidents/999999", headers=auth(token))
    assert response.status_code == 404
