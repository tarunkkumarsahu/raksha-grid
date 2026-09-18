from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_demo_scenario_is_explicitly_labelled_simulation():
    response = client.get("/demo/situation")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "simulation"
    assert "Synthetic" in body["notice"]
