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
        session.execute(delete(IncidentRoadLinkRecord))
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RoadEdgeRecord))
        session.execute(delete(RoadNodeRecord))
        session.execute(delete(NetworkMeta))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))
    yield
    with SessionLocal.begin() as session:
        session.execute(delete(IncidentRoadLinkRecord))
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RoadEdgeRecord))
        session.execute(delete(RoadNodeRecord))
        session.execute(delete(NetworkMeta))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register_and_login(email: str, role: str, verified_team: bool = True):
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
    login = client.post("/v1/auth/login", json={"email": email, "password": PASSWORD})
    assert login.status_code == 200
    return registered.json(), login.json()["access_token"]


def incident_payload():
    return {
        "category": "blocked_way",
        "title": "Bridge B12 is flooded",
        "description": "Field team reports the bridge is not passable.",
        "severity": "high",
        "latitude": 26.1,
        "longitude": 86.6,
        "photo_reference": "demo/b12.jpg",
        "gps_verified": True,
        "independent_corroborations": 2,
        "contradicting_reports": 0,
    }


def network_payload():
    return {
        "replace_existing": True,
        "nodes": [
            {"node_id": "RAMPUR", "label": "Rampur", "node_type": "settlement"},
            {"node_id": "B12", "label": "Bridge B12", "node_type": "bridge"},
            {"node_id": "SHELTER_A", "label": "Shelter A", "node_type": "shelter", "properties": {"capacity_remaining": 80}},
            {"node_id": "J3", "label": "Junction J3", "node_type": "junction"},
        ],
        "edges": [
            {"edge_id": "B12", "source_node_id": "RAMPUR", "target_node_id": "B12", "travel_minutes": 5, "base_risk": 0.1},
            {"edge_id": "SAFE", "source_node_id": "RAMPUR", "target_node_id": "J3", "travel_minutes": 6, "base_risk": 0.1},
            {"edge_id": "ALT", "source_node_id": "J3", "target_node_id": "SHELTER_A", "travel_minutes": 5, "base_risk": 0.1},
            {"edge_id": "B12-S", "source_node_id": "B12", "target_node_id": "SHELTER_A", "travel_minutes": 4, "base_risk": 0.1},
        ],
    }


def test_verified_incident_closes_edge_and_returns_reroute():
    _, team_token = register_and_login("team@example.com", "response_team")
    _, citizen_token = register_and_login("citizen@example.com", "citizen")
    imported = client.post("/v1/network/import", json=network_payload(), headers=auth(team_token))
    assert imported.status_code == 200

    created = client.post("/v1/incidents/reports", json=incident_payload(), headers=auth(team_token))
    assert created.status_code == 201
    incident_id = created.json()["id"]

    closed = client.post(
        f"/v1/incidents/{incident_id}/road-closure",
        json={
            "edge_id": "B12",
            "reason": "Bridge flooded; field team confirmed impassable.",
            "origin_node_id": "RAMPUR",
            "destination_node_id": "SHELTER_A",
        },
        headers=auth(team_token),
    )
    assert closed.status_code == 200
    body = closed.json()
    assert body["action"] == "closed"
    assert body["status"] == "blocked"
    assert body["rerouted"] is True
    assert body["route"]["path_nodes"] == ["RAMPUR", "J3", "SHELTER_A"]
    assert body["route"]["path_edges"] == ["SAFE", "ALT"]

    route = client.post(
        "/v1/network/route",
        json={"origin_node_id": "RAMPUR", "destination_node_id": "SHELTER_A"},
        headers=auth(citizen_token),
    )
    assert route.status_code == 200
    assert route.json()["path_edges"] == ["SAFE", "ALT"]

    detail = client.get(f"/v1/incidents/{incident_id}", headers=auth(citizen_token))
    assert detail.status_code == 200
    actions = [event["action"] for event in detail.json()["audit_events"]]
    assert "road_closed_from_incident" in actions


def test_citizen_cannot_close_roads_and_unverified_incident_cannot_close():
    _, citizen_token = register_and_login("citizen@example.com", "citizen")
    response = client.post(
        "/v1/incidents/999/road-closure",
        json={"edge_id": "B12", "reason": "x"},
        headers=auth(citizen_token),
    )
    assert response.status_code == 403

    _, team_token = register_and_login("team@example.com", "response_team")
    client.post("/v1/network/import", json=network_payload(), headers=auth(team_token))
    created = client.post(
        "/v1/incidents/reports",
        json={
            **incident_payload(),
            "independent_corroborations": 0,
            "photo_reference": None,
        },
        headers=auth(citizen_token),
    )
    assert created.status_code == 201
    response = client.post(
        f"/v1/incidents/{created.json()['id']}/road-closure",
        json={"edge_id": "B12", "reason": "not verified"},
        headers=auth(team_token),
    )
    assert response.status_code == 409


def test_reopen_restores_edge_and_increments_version():
    _, team_token = register_and_login("team@example.com", "response_team")
    client.post("/v1/network/import", json=network_payload(), headers=auth(team_token))
    created = client.post("/v1/incidents/reports", json=incident_payload(), headers=auth(team_token)).json()

    closed = client.post(
        f"/v1/incidents/{created['id']}/road-closure",
        json={"edge_id": "B12", "reason": "closure", "origin_node_id": "RAMPUR", "destination_node_id": "SHELTER_A"},
        headers=auth(team_token),
    ).json()
    assert closed["network_version"] == 2

    reopened = client.post(
        f"/v1/incidents/{created['id']}/road-reopen",
        json={"edge_id": "B12", "reason": "road inspected", "origin_node_id": "RAMPUR", "destination_node_id": "SHELTER_A"},
        headers=auth(team_token),
    )
    assert reopened.status_code == 200
    assert reopened.json()["action"] == "reopened"
    assert reopened.json()["status"] == "open"
    assert reopened.json()["network_version"] == 3
