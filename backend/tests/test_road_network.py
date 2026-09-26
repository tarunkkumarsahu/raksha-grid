import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.database import SessionLocal
from app.main import app
from app.models import (
    AuditEventRecord,
    IncidentRecord,
    IncidentReportRecord,
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
def clean_network_tables(monkeypatch):
    monkeypatch.setenv("RESPONSE_TEAM_REGISTRATION_CODE", TEAM_CODE)
    with SessionLocal.begin() as session:
        session.execute(delete(RoadEdgeRecord))
        session.execute(delete(RoadNodeRecord))
        session.execute(delete(NetworkMeta))
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))
    yield
    with SessionLocal.begin() as session:
        session.execute(delete(RoadEdgeRecord))
        session.execute(delete(RoadNodeRecord))
        session.execute(delete(NetworkMeta))
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))


def register_and_login(email: str, role: str, verified_team: bool = True):
    body = {
        "email": email,
        "display_name": "Network Tester",
        "password": PASSWORD,
        "role": role,
    }
    if role == "response_team" and verified_team:
        body["response_team_verification_code"] = TEAM_CODE
    registered = client.post("/v1/auth/register", json=body)
    assert registered.status_code == 201
    logged_in = client.post(
        "/v1/auth/login",
        json={"email": email, "password": PASSWORD},
    )
    assert logged_in.status_code == 200
    return registered.json(), logged_in.json()["access_token"]


def auth(token: str):
    return {"Authorization": f"Bearer {token}"}


def sample_network():
    return {
        "replace_existing": True,
        "nodes": [
            {"node_id": "A", "label": "Origin", "node_type": "settlement"},
            {"node_id": "B", "label": "Junction B", "node_type": "junction"},
            {"node_id": "C", "label": "Junction C", "node_type": "junction"},
            {"node_id": "D", "label": "Shelter", "node_type": "shelter"},
        ],
        "edges": [
            {
                "edge_id": "E1",
                "source_node_id": "A",
                "target_node_id": "B",
                "travel_minutes": 4,
                "base_risk": 0.05,
            },
            {
                "edge_id": "E2",
                "source_node_id": "B",
                "target_node_id": "D",
                "travel_minutes": 4,
                "base_risk": 0.05,
            },
            {
                "edge_id": "E3",
                "source_node_id": "A",
                "target_node_id": "C",
                "travel_minutes": 5,
                "base_risk": 0.10,
            },
            {
                "edge_id": "E4",
                "source_node_id": "C",
                "target_node_id": "D",
                "travel_minutes": 5,
                "base_risk": 0.10,
            },
        ],
    }


def test_network_endpoints_require_authentication():
    assert client.get("/v1/network").status_code == 401
    assert client.post(
        "/v1/network/route",
        json={"origin_node_id": "A", "destination_node_id": "D"},
    ).status_code == 401


def test_only_verified_response_team_can_import_network():
    _, citizen = register_and_login("citizen@example.com", "citizen")
    response = client.post(
        "/v1/network/import",
        json=sample_network(),
        headers=auth(citizen),
    )
    assert response.status_code == 403

    _, unverified_team = register_and_login(
        "pending-team@example.com",
        "response_team",
        verified_team=False,
    )
    response = client.post(
        "/v1/network/import",
        json=sample_network(),
        headers=auth(unverified_team),
    )
    assert response.status_code == 403


def test_imported_network_is_versioned_and_visible():
    team, token = register_and_login("team@example.com", "response_team")
    response = client.post(
        "/v1/network/import",
        json=sample_network(),
        headers=auth(token),
    )
    assert response.status_code == 200
    body = response.json()

    assert body["version"] == 1
    assert len(body["nodes"]) == 4
    assert len(body["edges"]) == 4
    assert all(edge["updated_by_user_id"] == team["id"] for edge in body["edges"])


def test_routing_uses_lowest_risk_weighted_cost_and_reroutes_after_closure():
    _, team_token = register_and_login("team@example.com", "response_team")
    _, citizen_token = register_and_login("citizen@example.com", "citizen")

    client.post(
        "/v1/network/import",
        json=sample_network(),
        headers=auth(team_token),
    )

    first = client.post(
        "/v1/network/route",
        json={"origin_node_id": "A", "destination_node_id": "D"},
        headers=auth(citizen_token),
    )
    assert first.status_code == 200
    first_body = first.json()
    assert first_body["path_nodes"] == ["A", "B", "D"]
    assert first_body["path_edges"] == ["E1", "E2"]
    assert first_body["network_version"] == 1

    closed = client.patch(
        "/v1/network/edges/E2",
        json={"status": "blocked", "current_risk": 1.0},
        headers=auth(team_token),
    )
    assert closed.status_code == 200
    assert closed.json()["status"] == "blocked"

    rerouted = client.post(
        "/v1/network/route",
        json={"origin_node_id": "A", "destination_node_id": "D"},
        headers=auth(citizen_token),
    )
    assert rerouted.status_code == 200
    body = rerouted.json()
    assert body["path_nodes"] == ["A", "C", "D"]
    assert body["path_edges"] == ["E3", "E4"]
    assert body["network_version"] == 2


def test_multiple_closures_return_no_viable_route():
    _, team_token = register_and_login("team@example.com", "response_team")
    _, citizen_token = register_and_login("citizen@example.com", "citizen")
    client.post("/v1/network/import", json=sample_network(), headers=auth(team_token))

    client.patch(
        "/v1/network/edges/E2",
        json={"status": "blocked"},
        headers=auth(team_token),
    )
    client.patch(
        "/v1/network/edges/E4",
        json={"status": "blocked"},
        headers=auth(team_token),
    )

    response = client.post(
        "/v1/network/route",
        json={"origin_node_id": "A", "destination_node_id": "D"},
        headers=auth(citizen_token),
    )
    assert response.status_code == 422
    assert "No viable route" in response.json()["detail"]


def test_edge_status_change_increments_network_version():
    _, team_token = register_and_login("team@example.com", "response_team")
    _, citizen_token = register_and_login("citizen@example.com", "citizen")
    client.post("/v1/network/import", json=sample_network(), headers=auth(team_token))

    client.patch(
        "/v1/network/edges/E1",
        json={"status": "restricted", "current_risk": 0.6},
        headers=auth(team_token),
    )
    snapshot = client.get("/v1/network", headers=auth(citizen_token))
    assert snapshot.status_code == 200
    assert snapshot.json()["version"] == 2


def test_import_rejects_edges_that_reference_unknown_nodes():
    _, token = register_and_login("team@example.com", "response_team")
    payload = sample_network()
    payload["edges"].append(
        {
            "edge_id": "BAD",
            "source_node_id": "A",
            "target_node_id": "MISSING",
            "travel_minutes": 2,
        }
    )

    response = client.post(
        "/v1/network/import",
        json=payload,
        headers=auth(token),
    )
    assert response.status_code == 422


def test_one_way_edge_is_not_used_in_reverse():
    _, team_token = register_and_login("team@example.com", "response_team")
    _, citizen_token = register_and_login("citizen@example.com", "citizen")
    payload = {
        "replace_existing": True,
        "nodes": [
            {"node_id": "A", "label": "A", "node_type": "junction"},
            {"node_id": "B", "label": "B", "node_type": "junction"},
        ],
        "edges": [
            {
                "edge_id": "ONE",
                "source_node_id": "A",
                "target_node_id": "B",
                "bidirectional": False,
                "travel_minutes": 3,
            }
        ],
    }
    client.post("/v1/network/import", json=payload, headers=auth(team_token))

    forward = client.post(
        "/v1/network/route",
        json={"origin_node_id": "A", "destination_node_id": "B"},
        headers=auth(citizen_token),
    )
    assert forward.status_code == 200

    reverse = client.post(
        "/v1/network/route",
        json={"origin_node_id": "B", "destination_node_id": "A"},
        headers=auth(citizen_token),
    )
    assert reverse.status_code == 422
