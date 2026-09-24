from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def setup_function():
    assert client.post("/demo/reset").status_code == 200


def test_simulated_isolation_changes_when_bridge_blocked():
    before = client.get("/demo/state").json()
    assert before["mode"] == "simulation"
    assert "fictional" in before["notice"]
    initial = next(s for s in before["priority_settlements"] if s["id"] == "rampur")
    assert initial["usable_exits"] == 2
    assert initial["time_to_isolation_minutes"] == 37
    assert initial["recommended_route"]["shelter_id"] == "shelter-a"

    report_response = client.post("/demo/reports", json={
        "road_id": "BR-12",
        "reporter_role": "responder",
        "observation": "bridge_submerged",
        "note": "Synthetic exercise",
    })
    assert report_response.status_code == 201
    pending = next(r for r in client.get("/demo/state").json()["roads"] if r["id"] == "BR-12")
    assert pending["blocked"] is False  # A claim does not close the road automatically.

    reviewed = client.post("/demo/reports/REP-0001/review", json={
        "reviewer_role": "officer", "decision": "confirm_blocked"})
    assert reviewed.status_code == 200
    after = reviewed.json()["state"]
    rampur = next(s for s in after["priority_settlements"] if s["id"] == "rampur")
    assert rampur["usable_exits"] == 1
    assert rampur["time_to_isolation_minutes"] == 21
    assert rampur["recommended_route"]["shelter_id"] == "shelter-b"
    assert "Bridge junction" not in rampur["recommended_route"]["path_labels"]
    assert client.post("/demo/reports/REP-0001/review", json={
        "reviewer_role": "officer", "decision": "confirm_blocked"}).status_code == 409


def test_last_road_closure_leaves_no_route_and_isolation_now():
    for road_id, report_id in [("BR-12", "REP-0001"), ("R-08", "REP-0002")]:
        submitted = client.post("/demo/reports", json={
            "road_id": road_id, "reporter_role": "responder",
            "observation": "road_flooded"})
        assert submitted.status_code == 201
        assert client.post(f"/demo/reports/{report_id}/review", json={
            "reviewer_role": "officer", "decision": "confirm_blocked"}).status_code == 200
    rampur = next(s for s in client.get("/demo/state").json()["priority_settlements"]
                  if s["id"] == "rampur")
    assert rampur["time_to_isolation_minutes"] == 0
    assert rampur["usable_exits"] == 0
    assert rampur["recommended_route"] is None
    assert rampur["is_isolated"] is True


def test_rejected_report_does_not_block_a_road():
    assert client.post("/demo/reports", json={
        "road_id": "BR-12", "reporter_role": "citizen",
        "observation": "road_flooded"}).status_code == 201
    state = client.post("/demo/reports/REP-0001/review", json={
        "reviewer_role": "officer", "decision": "reject_report"}).json()["state"]
    assert not any(r["blocked"] for r in state["roads"])


def test_invalid_road_is_rejected():
    response = client.post("/demo/reports", json={
        "road_id": "NOT-A-ROAD", "reporter_role": "responder",
        "observation": "road_flooded"})
    assert response.status_code == 404
