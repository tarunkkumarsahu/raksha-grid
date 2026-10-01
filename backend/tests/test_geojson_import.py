import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.database import SessionLocal
from app.main import app
from app.models import NetworkMeta, NotificationRecord, RoadEdgeRecord, RoadNodeRecord, UserRecord, RefreshTokenRecord


client = TestClient(app)
PASSWORD = "StrongPass123!"
TEAM_CODE = "verified-team-code"


@pytest.fixture(autouse=True)
def clean_tables(monkeypatch):
    monkeypatch.setenv("RESPONSE_TEAM_REGISTRATION_CODE", TEAM_CODE)
    with SessionLocal.begin() as session:
        session.execute(delete(RoadEdgeRecord))
        session.execute(delete(RoadNodeRecord))
        session.execute(delete(NetworkMeta))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))
    yield
    with SessionLocal.begin() as session:
        session.execute(delete(RoadEdgeRecord))
        session.execute(delete(RoadNodeRecord))
        session.execute(delete(NetworkMeta))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))


def auth(token: str):
    return {"Authorization": f"Bearer {token}"}


def team_token():
    body = {
        "email": "team@example.com",
        "display_name": "GIS Team",
        "password": PASSWORD,
        "role": "response_team",
        "response_team_verification_code": TEAM_CODE,
    }
    assert client.post("/v1/auth/register", json=body).status_code == 201
    login = client.post("/v1/auth/login", json={"email": body["email"], "password": PASSWORD})
    assert login.status_code == 200
    return login.json()["access_token"]


def test_geojson_import_builds_network_with_geometry_and_coordinates():
    token = team_token()
    payload = {
        "type": "FeatureCollection",
        "replace_existing": True,
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [86.60, 26.12]},
                "properties": {
                    "node_id": "RAMPUR",
                    "label": "Rampur",
                    "node_type": "settlement",
                    "district": "Supaul",
                    "data_mode": "simulation",
                },
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [86.61, 26.13]},
                "properties": {
                    "node_id": "SHELTER_A",
                    "label": "Shelter A",
                    "node_type": "shelter",
                    "capacity_total": 100,
                    "capacity_remaining": 100,
                },
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[86.60, 26.12], [86.61, 26.13]],
                },
                "properties": {
                    "edge_id": "R1",
                    "source_node_id": "RAMPUR",
                    "target_node_id": "SHELTER_A",
                    "travel_minutes": 8,
                    "base_risk": 0.15,
                },
            },
        ],
    }
    response = client.post("/v1/network/import/geojson", json=payload, headers=auth(token))
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == 1
    assert body["nodes"][0]["latitude"] is not None
    assert body["edges"][0]["geometry_geojson"]["type"] == "LineString"


def test_bihar_demo_endpoint_is_explicitly_synthetic():
    token = team_token()
    response = client.post("/v1/network/import/demo-bihar", headers=auth(token))
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == 1
    labels = {node["label"] for node in body["nodes"]}
    assert {"Rampur", "Basantpur", "Sonapur", "Shelter A", "Shelter B"} <= labels
