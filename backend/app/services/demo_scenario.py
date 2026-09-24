import networkx as nx

from app.schemas import (
    GroundReportInput,
    RouteEdge,
    SafeCorridorRequest,
    SettlementInput,
)
from app.services.ground_intel import score_ground_report
from app.services.isolation import compute_isolation_intelligence
from app.services.routing import find_safe_corridor


class DemoScenario:
    """Stateful Round-1 demo scenario.

    This is intentionally labelled SIMULATION. It demonstrates how a verified
    field report can change road status, settlement isolation risk, shelter
    choice and role-specific guidance.
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> dict:
        self.blocked_roads: set[str] = set()
        self.last_report: dict | None = None
        return self.snapshot()

    def _road_edges(self) -> list[RouteEdge]:
        roads = [
            RouteEdge(source="Rampur", target="Bridge_B12", travel_minutes=4, hazard_risk=0.10),
            RouteEdge(source="Bridge_B12", target="Shelter_A", travel_minutes=5, hazard_risk=0.08),
            RouteEdge(source="Rampur", target="Road_R12", travel_minutes=6, hazard_risk=0.22),
            RouteEdge(source="Road_R12", target="Shelter_B", travel_minutes=8, hazard_risk=0.12),
            RouteEdge(source="Road_R12", target="Hospital_H1", travel_minutes=6, hazard_risk=0.10),
        ]
        for edge in roads:
            road_id = self._road_id(edge.source, edge.target)
            edge.blocked = road_id in self.blocked_roads
        return roads

    @staticmethod
    def _road_id(a: str, b: str) -> str:
        pair = frozenset((a, b))
        if pair == frozenset(("Rampur", "Bridge_B12")):
            return "B12"
        if pair == frozenset(("Bridge_B12", "Shelter_A")):
            return "R11"
        if pair == frozenset(("Rampur", "Road_R12")):
            return "R12"
        if pair == frozenset(("Road_R12", "Shelter_B")):
            return "R13"
        if pair == frozenset(("Road_R12", "Hospital_H1")):
            return "R14"
        return f"{a}-{b}"

    def _route(self, destination: str) -> dict | None:
        req = SafeCorridorRequest(
            origin="Rampur",
            destination=destination,
            edges=self._road_edges(),
        )
        try:
            result = find_safe_corridor(req)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
        return result.model_dump()

    def _isolation(self):
        if "B12" in self.blocked_roads:
            exit_failures = [37]
            route_risk = 0.62
            shelter_accessibility = 0.55
        else:
            exit_failures = [37, 82]
            route_risk = 0.28
            shelter_accessibility = 0.90

        item = SettlementInput(
            id="VIL-RAMPUR",
            name="Rampur",
            population=1840,
            vulnerable_population=510,
            flood_risk=0.88,
            route_risk=route_risk,
            medical_urgency=0.35,
            shelter_accessibility=shelter_accessibility,
            predicted_exit_failure_minutes=exit_failures,
            data_mode="simulation",
        )
        return compute_isolation_intelligence(item)

    def snapshot(self) -> dict:
        shelter_a = self._route("Shelter_A")
        shelter_b = self._route("Shelter_B")
        isolation = self._isolation()

        if shelter_a and shelter_b:
            chosen_name, chosen_route = min(
                [("Shelter A", shelter_a), ("Shelter B", shelter_b)],
                key=lambda x: x[1]["weighted_cost"],
            )
        elif shelter_a:
            chosen_name, chosen_route = "Shelter A", shelter_a
        elif shelter_b:
            chosen_name, chosen_route = "Shelter B", shelter_b
        else:
            chosen_name, chosen_route = "No reachable shelter", None

        blocked = sorted(self.blocked_roads)
        route_nodes = chosen_route["path"] if chosen_route else []

        return {
            "mode": "simulation",
            "notice": "Round-1 synthetic scenario. Do not present this as live official data.",
            "event": "Flood response demo - Rampur",
            "blocked_roads": blocked,
            "last_report": self.last_report,
            "citizen": {
                "location": "Rampur",
                "risk": isolation.priority_band,
                "time_to_isolation_minutes": isolation.time_to_isolation_minutes,
                "recommended_shelter": chosen_name,
                "route": route_nodes,
                "travel_minutes": chosen_route["travel_minutes"] if chosen_route else None,
                "route_risk": chosen_route["route_risk"] if chosen_route else None,
                "message": (
                    "Use the updated evacuation route."
                    if blocked
                    else "A safe evacuation route is currently available."
                ),
            },
            "responder": {
                "mission": "Rampur evacuation support",
                "priority": isolation.priority_band,
                "population_exposed": 1840,
                "safe_exits_remaining": isolation.safe_exits_remaining,
                "approach_route": route_nodes,
                "message": (
                    "Bridge B12 is blocked. Approach through Road R12."
                    if "B12" in blocked
                    else "Primary approach remains available."
                ),
            },
            "officer": {
                "settlement": "Rampur",
                "priority_score": isolation.priority_score,
                "priority_band": isolation.priority_band,
                "time_to_isolation_minutes": isolation.time_to_isolation_minutes,
                "safe_exits_remaining": isolation.safe_exits_remaining,
                "recommended_shelter": chosen_name,
                "blocked_roads": blocked,
                "explanation": isolation.explanation,
            },
        }

    def report_blocked_road(
        self,
        road_id: str,
        report: GroundReportInput,
        reason: str = "Flooded / blocked",
    ) -> dict:
        confidence = score_ground_report(report)
        accepted = confidence.state == "actionable"

        self.last_report = {
            "road_id": road_id,
            "reason": reason,
            "confidence": confidence.confidence,
            "state": confidence.state,
            "accepted": accepted,
            "evidence": confidence.evidence,
        }

        if accepted:
            self.blocked_roads.add(road_id)

        result = self.snapshot()
        result["report_result"] = self.last_report
        return result


demo_scenario = DemoScenario()
