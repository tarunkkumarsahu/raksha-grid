from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_round1_demo_changes_after_verified_bridge_report():
    reset = client.post("/demo/round1/reset")
    assert reset.status_code == 200
    before = reset.json()

    assert before["mode"] == "simulation"
    assert before["citizen"]["recommended_shelter"] == "Shelter A"
    assert before["officer"]["safe_exits_remaining"] == 2
    assert before["blocked_roads"] == []

    response = client.post(
        "/demo/round1/report-road",
        json={
            "road_id": "B12",
            "reason": "Bridge submerged",
            "reporter_role": "responder",
            "gps_verified": True,
            "photo_attached": True,
            "independent_corroborations": 2,
            "age_minutes": 2,
            "contradicting_reports": 0,
        },
    )
    assert response.status_code == 200
    after = response.json()

    assert after["report_result"]["accepted"] is True
    assert "B12" in after["blocked_roads"]
    assert after["citizen"]["recommended_shelter"] == "Shelter B"
    assert after["officer"]["safe_exits_remaining"] == 1
    assert after["officer"]["time_to_isolation_minutes"] == 37
    assert "Road_R12" in after["citizen"]["route"]
    assert "Bridge B12 is blocked" in after["responder"]["message"]


def test_low_confidence_report_does_not_block_road():
    client.post("/demo/round1/reset")

    response = client.post(
        "/demo/round1/report-road",
        json={
            "road_id": "B12",
            "reporter_role": "citizen",
            "gps_verified": False,
            "photo_attached": False,
            "independent_corroborations": 0,
            "age_minutes": 40,
            "contradicting_reports": 0,
        },
    )
    assert response.status_code == 200
    body = response.json()

    assert body["report_result"]["accepted"] is False
    assert body["blocked_roads"] == []
    assert body["citizen"]["recommended_shelter"] == "Shelter A"
