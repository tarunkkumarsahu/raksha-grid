"""Round-1 scenario regression tests: every case resets shared in-memory state."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def reset():
    response = client.post("/demo/round1/reset")
    assert response.status_code == 200
    return response.json()


def report(road_id="B12", **overrides):
    body = {
        "road_id": road_id, "reason": "Flooded bridge",
        "reporter_role": "responder", "gps_verified": True,
        "photo_attached": True, "independent_corroborations": 2,
        "age_minutes": 2, "contradicting_reports": 0,
    }
    body.update(overrides)
    return client.post("/demo/round1/report-road", json=body)


def test_graph_has_three_settlements_and_eleven_road_segments():
    state = reset()
    assert len(state["roads"]) >= 10
    assert len(state["settlements"]) == 3
    assert len(state["shelters"]) == 2
    assert state["citizen"]["recommended_shelter"] == "Shelter A"
    assert state["officer"]["safe_exits_remaining"] == 2
    assert state["mode"] == "simulation"


def test_second_road_closure_makes_rampur_unreachable_without_fabricating_route():
    reset()
    first = report("B12").json()
    assert first["citizen"]["recommended_shelter"] == "Shelter B"
    assert first["officer"]["safe_exits_remaining"] == 1
    second = report("R12").json()
    assert second["citizen"]["recommended_shelter"] == "No reachable shelter"
    assert second["citizen"]["route"] == []
    assert second["citizen"]["travel_minutes"] is None
    assert second["citizen"]["route_status"] == "unavailable"
    assert second["officer"]["safe_exits_remaining"] == 0
    assert second["officer"]["time_to_isolation_minutes"] == 0
    assert "DO NOT proceed" in second["responder"]["message"]


def test_shelter_capacity_recommends_other_reachable_shelter():
    reset()
    full = client.patch("/demo/round1/shelters/Shelter_A/capacity",
                        json={"capacity_remaining": 0})
    assert full.status_code == 200
    assert full.json()["citizen"]["recommended_shelter"] == "Shelter B"
    second = client.patch("/demo/round1/shelters/Shelter_B/capacity",
                          json={"capacity_remaining": 0}).json()
    assert second["citizen"]["recommended_shelter"] == "No reachable shelter"
    assert second["citizen"]["route"] == []


def test_nearly_full_shelter_is_not_recommended_for_group():
    reset()
    updated = client.patch("/demo/round1/shelters/Shelter_A/capacity",
                           json={"capacity_remaining": 20}).json()
    assert updated["citizen"]["recommended_shelter"] == "Shelter B"


def test_unknown_road_and_shelter_are_rejected_without_state_change():
    before = reset()
    response = report("DOES_NOT_EXIST")
    assert response.status_code == 422
    result = client.patch("/demo/round1/shelters/INVALID/capacity",
                          json={"capacity_remaining": 0})
    assert result.status_code == 422
    after = client.get("/demo/round1").json()
    assert after["version"] == before["version"]
    assert after["blocked_roads"] == []


def test_low_confidence_report_does_not_close_road():
    reset()
    result = report("B12", reporter_role="citizen", gps_verified=False,
                    photo_attached=False, independent_corroborations=0,
                    age_minutes=40).json()
    assert result["report_result"]["accepted"] is False
    assert "B12" not in result["blocked_roads"]


def test_citizen_report_stays_pending_until_demo_officer_reviews():
    reset()
    state = report("B12", reporter_role="citizen", gps_verified=True,
                   photo_attached=True, independent_corroborations=2,
                   age_minutes=0).json()
    entry = state["report_result"]
    assert entry["status"] == "pending"
    assert state["blocked_roads"] == []
    reviewed = client.post(
        f"/demo/round1/reports/{entry['report_id']}/review",
        json={"approve": True},
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["citizen"]["recommended_shelter"] == "Shelter B"
    assert "B12" in reviewed.json()["blocked_roads"]
    assert client.post(
        f"/demo/round1/reports/{entry['report_id']}/review",
        json={"approve": True},
    ).status_code == 422


def test_contradictory_responder_report_requires_review_and_can_be_rejected():
    reset()
    result = report("B12", contradicting_reports=1).json()
    assert result["report_result"]["status"] == "pending"
    assert result["blocked_roads"] == []
    reviewed = client.post(
        f"/demo/round1/reports/{result['report_result']['report_id']}/review",
        json={"approve": False},
    ).json()
    assert reviewed["blocked_roads"] == []
    assert reviewed["last_report"]["status"] == "rejected"


def test_role_views_share_state_and_change_version_on_accepted_report():
    before = reset()
    after = report("B12").json()
    assert after["version"] > before["version"]
    fetched = client.get("/demo/round1").json()
    assert fetched["version"] == after["version"]
    assert fetched["citizen"]["route"] == after["citizen"]["route"]
    assert fetched["officer"]["blocked_roads"] == after["blocked_roads"]
    assert fetched["responder"]["safe_exits_remaining"] == 1
