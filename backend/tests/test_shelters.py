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
            IncidentRoadLinkRecord,
            AuditEventRecord,
            IncidentReportRecord,
            IncidentRecord,
            RoadEdgeRecord,
            RoadNodeRecord,
            NetworkMeta,
            NotificationRecord,
            RefreshTokenRecord,
            NotificationRecord,
            UserRecord,
        ):
            session.execute(delete(model))
    yield
    with SessionLocal.begin() as session:
        for model in (
            IncidentRoadLinkRecord,
            AuditEventRecord,
            IncidentReportRecord,
            IncidentRecord,
            RoadEdgeRecord,
            RoadNodeRecord,
            NetworkMeta,
            RefreshTokenRecord,
            NotificationRecord,
            UserRecord,
        ):
            session.execute(delete(model))


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register_and_login(email: str, role: str, verified_team: bool = True):
    body = {"email": email, "display_name": "Test User", "password": PASSWORD, "role": role}
    if role == "response_team" and verified_team:
        body["response_team_verification_code"] = TEAM_CODE
    assert client.post("/v1/auth/register", json=body).status_code == 201
    login = client.post("/v1/auth/login", json={"email": email, "password": PASSWORD})
    assert login.status_code == 200
    return login.json()["access_token"]


def network_payload():
    return {
        "replace_existing": True,
        "nodes": [
            {"node_id": "RAMPUR", "label": "Rampur", "node_type": "settlement"},
            {"node_id": "S1", "label": "Shelter A", "node_type": "shelter", "properties": {"capacity_total": 50, "capacity_remaining": 50}},
            {"node_id": "S2", "label": "Shelter B", "node_type": "shelter", "properties": {"capacity_total": 120, "capacity_remaining": 120}},
        ],
        "edges": [
            {"edge_id": "E1", "source_node_id": "RAMPUR", "target_node_id": "S1", "travel_minutes": 8, "base_risk": 0.2},
            {"edge_id": "E2", "source_node_id": "RAMPUR", "target_node_id": "S2", "travel_minutes": 12, "base_risk": 0.05},
        ],
    }


def test_capacity_update_changes_allocation_and_is_response_team_only():
    team = register_and_login("team@example.com", "response_team")
    citizen = register_and_login("citizen@example.com", "citizen")
    assert client.post("/v1/network/import", json=network_payload(), headers=auth(team)).status_code == 200

    first = client.post(
        "/v1/shelters/allocate",
        json={"origin_node_id": "RAMPUR", "people_count": 40},
        headers=auth(citizen),
    )
    assert first.status_code == 200
    assert first.json()["selected_shelter"]["node_id"] == "S1"

    forbidden = client.patch(
        "/v1/shelters/S1/capacity",
        json={"capacity_remaining": 0, "reason": "filled"},
        headers=auth(citizen),
    )
    assert forbidden.status_code == 403

    updated = client.patch(
        "/v1/shelters/S1/capacity",
        json={"capacity_remaining": 0, "reason": "shelter filled"},
        headers=auth(team),
    )
    assert updated.status_code == 200
    assert updated.json()["availability"] == "full"

    second = client.post(
        "/v1/shelters/allocate",
        json={"origin_node_id": "RAMPUR", "people_count": 40},
        headers=auth(citizen),
    )
    assert second.status_code == 200
    assert second.json()["selected_shelter"]["node_id"] == "S2"
