from app.schemas import (
    GroundReportInput,
    RouteEdge,
    SafeCorridorRequest,
    SettlementInput,
)
from app.services.ground_intel import score_ground_report
from app.services.isolation import compute_isolation_intelligence
from app.services.routing import find_safe_corridor


def test_single_exit_settlement_becomes_critical_earlier():
    fragile = SettlementInput(
        id="B",
        name="Village B",
        population=1200,
        vulnerable_population=350,
        flood_risk=0.85,
        route_risk=0.75,
        medical_urgency=0.2,
        shelter_accessibility=0.5,
        predicted_exit_failure_minutes=[35],
    )
    resilient = SettlementInput(
        id="A",
        name="Village A",
        population=4500,
        vulnerable_population=700,
        flood_risk=0.8,
        route_risk=0.4,
        medical_urgency=0.2,
        shelter_accessibility=0.8,
        predicted_exit_failure_minutes=[40, 75, 100],
    )

    b = compute_isolation_intelligence(fragile)
    a = compute_isolation_intelligence(resilient)

    assert b.safe_exits_remaining == 1
    assert b.time_to_isolation_minutes == 35
    assert b.priority_score > a.priority_score


def test_safe_corridor_can_choose_longer_but_safer_route():
    request = SafeCorridorRequest(
        origin="A",
        destination="D",
        edges=[
            RouteEdge(source="A", target="B", travel_minutes=4, hazard_risk=0.9),
            RouteEdge(source="B", target="D", travel_minutes=4, hazard_risk=0.8),
            RouteEdge(source="A", target="C", travel_minutes=7, hazard_risk=0.05),
            RouteEdge(source="C", target="D", travel_minutes=7, hazard_risk=0.05),
        ],
    )

    result = find_safe_corridor(request)
    assert result.path == ["A", "C", "D"]
    assert result.travel_minutes == 14
    assert result.route_risk < 0.2


def test_responder_report_with_evidence_becomes_actionable():
    report = GroundReportInput(
        reporter_role="responder",
        gps_verified=True,
        photo_attached=True,
        independent_corroborations=2,
        age_minutes=3,
    )
    result = score_ground_report(report)
    assert result.state == "actionable"
    assert result.confidence >= 0.75
