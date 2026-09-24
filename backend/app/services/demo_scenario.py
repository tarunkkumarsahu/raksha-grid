"""Round-1 DISASTER SIMULATION, not a real evacuation or flood forecast.

All locations, road travel times, flood exposure, and expected failure times in
this module are invented for a repeatable demo. No actual GPS/shelter verification
is performed. State is in-memory and shared only within one Uvicorn worker.
"""
from copy import deepcopy
from threading import RLock

import networkx as nx

from app.schemas import GroundReportInput, RouteEdge, SafeCorridorRequest, SettlementInput
from app.services.ground_intel import score_ground_report
from app.services.isolation import compute_isolation_intelligence
from app.services.routing import find_safe_corridor


# Eleven segments, three settlements, two shelters, and a hospital.
# Coordinate-free graph: these node names are NOT geocoded locations.
ROADS = {
    "B12": ("Rampur", "Bridge_B12", 4, 0.10, 82),
    "R11": ("Bridge_B12", "Shelter_A", 5, 0.08, 80),
    "R12": ("Rampur", "Road_R12", 6, 0.22, 37),
    "R13": ("Road_R12", "Shelter_B", 8, 0.12, 60),
    "R14": ("Road_R12", "Hospital_H1", 6, 0.10, 67),
    "R21": ("Basantpur", "Bridge_B12", 5, 0.14, 72),
    "R22": ("Basantpur", "Junction_J3", 8, 0.15, 46),
    "R23": ("Junction_J3", "Road_R12", 4, 0.14, 52),
    "R31": ("Sonapur", "Junction_J3", 4, 0.19, 48),
    "R32": ("Sonapur", "Bridge_B12", 10, 0.13, 76),
    "R33": ("Junction_J3", "Shelter_A", 11, 0.32, 59),
}
SETTLEMENTS = {
    "Rampur": {"population": 1840, "vulnerable": 510, "evacuees": 40, "flood_risk": 0.88},
    "Basantpur": {"population": 1160, "vulnerable": 200, "evacuees": 25, "flood_risk": 0.71},
    "Sonapur": {"population": 720, "vulnerable": 130, "evacuees": 15, "flood_risk": 0.63},
}
SHELTERS = {"Shelter_A": {"name": "Shelter A", "capacity": 50},
            "Shelter_B": {"name": "Shelter B", "capacity": 120}}


class DemoScenario:
    def __init__(self) -> None:
        self._lock = RLock()
        self.version = 0
        self.reset()

    def reset(self) -> dict:
        with self._lock:
            self.blocked_roads: set[str] = set()
            self.shelter_capacity = {k: v["capacity"] for k, v in SHELTERS.items()}
            self.reports: list[dict] = []
            self.last_report: dict | None = None
            self.version += 1
            return self._snapshot()

    def _edges(self) -> list[RouteEdge]:
        return [RouteEdge(source=a, target=b, travel_minutes=t, hazard_risk=r,
                          blocked=road_id in self.blocked_roads)
                for road_id, (a, b, t, r, _failure) in ROADS.items()]

    def _graph(self) -> nx.Graph:
        graph = nx.Graph()
        for road_id, (a, b, t, risk, failure) in ROADS.items():
            if road_id not in self.blocked_roads:
                graph.add_edge(a, b, id=road_id, time=t, risk=risk, failure=failure)
        return graph

    def _routes(self, origin: str) -> list[dict]:
        candidates = []
        for shelter_id, remaining in self.shelter_capacity.items():
            if remaining < SETTLEMENTS[origin]["evacuees"]:
                continue
            try:
                route = find_safe_corridor(
                    SafeCorridorRequest(origin=origin, destination=shelter_id, edges=self._edges())
                )
                candidates.append({"shelter_id": shelter_id, "name": SHELTERS[shelter_id]["name"],
                                   **route.model_dump()})
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
        return sorted(candidates, key=lambda c: c["weighted_cost"])

    def _access(self, origin: str) -> tuple[int, float]:
        graph = self._graph()
        shelters = [s for s in SHELTERS if self.shelter_capacity[s] >= SETTLEMENTS[origin]["evacuees"]]
        failures = []
        if origin not in graph:
            return 0, 0.0
        for neighbor in graph.neighbors(origin):
            trial = graph.copy()
            trial.remove_node(origin)
            if neighbor in trial and any(
                s in trial and nx.has_path(trial, neighbor, s) for s in shelters
            ):
                failures.append(graph[origin][neighbor]["failure"])
        return len(failures), float(max(failures)) if failures else 0.0

    def _settlement(self, origin: str) -> dict:
        info = SETTLEMENTS[origin]
        exits, last_exit_minutes = self._access(origin)
        routes = self._routes(origin)
        # The horizon is a scenario input, not ML-derived or a validated forecast.
        # Actual graph connectivity determines exit availability.
        risk = compute_isolation_intelligence(SettlementInput(
            id="DEMO-" + origin.upper(), name=origin, population=info["population"],
            vulnerable_population=info["vulnerable"], flood_risk=info["flood_risk"],
            route_risk=0.65 if exits <= 1 else 0.28, medical_urgency=0.25,
            shelter_accessibility=0.75 if routes else 0.0,
            predicted_exit_failure_minutes=[last_exit_minutes] * exits,
            data_mode="simulation",
        ))
        chosen = routes[0] if routes else None
        return {
            "settlement": origin, "population_exposed": info["population"],
            "people_to_evacuate_demo": info["evacuees"],
            "safe_exits_remaining": exits, "time_to_isolation_minutes": last_exit_minutes,
            "priority_score": risk.priority_score, "priority_band": risk.priority_band,
            "explanation": risk.explanation,
            "recommended_shelter": chosen["name"] if chosen else "No reachable shelter",
            "shelter_id": chosen["shelter_id"] if chosen else None,
            "route": chosen["path"] if chosen else [],
            "travel_minutes": chosen["travel_minutes"] if chosen else None,
            "route_risk": chosen["route_risk"] if chosen else None,
            "route_status": "available" if chosen else "unavailable",
        }

    def _snapshot(self) -> dict:
        villages = {name: self._settlement(name) for name in SETTLEMENTS}
        rampur = villages["Rampur"]
        ordered = sorted(villages.values(), key=lambda v: v["priority_score"], reverse=True)
        if rampur["route_status"] == "unavailable":
            message = "NO VERIFIED EVACUATION ROUTE. Contact local emergency services and follow official advice."
        elif self.blocked_roads:
            message = "Route recalculated after a reported road closure. Seek official confirmation."
        else:
            message = "A modelled evacuation route is available. Check official instructions."

        return deepcopy({
            "mode": "simulation",
            "notice": "ALL locations, reports, capacities and predicted times are synthetic; route is NOT certified safe.",
            "version": self.version,
            "event": "Round-1 demo - synthetic flood scenario",
            "blocked_roads": sorted(self.blocked_roads),
            "roads": [{"id": k, "source": v[0], "target": v[1], "blocked": k in self.blocked_roads}
                      for k, v in ROADS.items()],
            "shelters": [{"id": sid, "name": SHELTERS[sid]["name"], "capacity_remaining": cap}
                         for sid, cap in self.shelter_capacity.items()],
            "settlements": villages,
            "last_report": self.last_report,
            "reports": self.reports,
            "citizen": {
                "location": "Rampur", "risk": rampur["priority_band"],
                "time_to_isolation_minutes": rampur["time_to_isolation_minutes"],
                "recommended_shelter": rampur["recommended_shelter"],
                "route": rampur["route"], "travel_minutes": rampur["travel_minutes"],
                "route_risk": rampur["route_risk"], "route_status": rampur["route_status"],
                "message": message,
            },
            "responder": {
                "mission": "Rampur evacuation support", "priority": rampur["priority_band"],
                "population_exposed": rampur["population_exposed"],
                "safe_exits_remaining": rampur["safe_exits_remaining"],
                "approach_route": rampur["route"],
                "message": ("No usable route in the model. Do NOT proceed without official direction."
                            if rampur["route_status"] == "unavailable" else
                            "Bridge B12 is blocked. Approach through Road R12."
                            if "B12" in self.blocked_roads else "Check current route and official field status."),
            },
            "officer": {
                "settlement": "Rampur", "priority_score": rampur["priority_score"],
                "priority_band": rampur["priority_band"],
                "time_to_isolation_minutes": rampur["time_to_isolation_minutes"],
                "safe_exits_remaining": rampur["safe_exits_remaining"],
                "recommended_shelter": rampur["recommended_shelter"],
                "blocked_roads": sorted(self.blocked_roads), "explanation": rampur["explanation"],
                "priority_settlements": ordered,
                "pending_reports": [r for r in self.reports if r["status"] == "pending"],
            },
        })

    def snapshot(self) -> dict:
        with self._lock:
            return self._snapshot()

    def report_blocked_road(self, road_id: str, report: GroundReportInput,
                            reason: str = "Flooded / blocked") -> dict:
        if road_id not in ROADS:
            raise ValueError("Unknown demo road ID.")
        with self._lock:
            score = score_ground_report(report)
            # Contradictory evidence requires human review, even for high-score reports.
            auto_accept = (score.state == "actionable" and report.reporter_role in
                           {"responder", "officer"} and report.contradicting_reports == 0)
            pending = not auto_accept and score.confidence >= 0.25
            status = "accepted" if auto_accept else "pending" if pending else "rejected"
            entry = {
                "report_id": len(self.reports) + 1, "road_id": road_id, "reason": reason,
                "confidence": score.confidence, "state": score.state,
                "accepted": auto_accept, "status": status, "evidence": score.evidence,
            }
            self.reports.append(entry)
            self.last_report = entry
            if auto_accept:
                self.blocked_roads.add(road_id)
            self.version += 1
            result = self._snapshot()
            result["report_result"] = deepcopy(entry)
            return result

    def review_report(self, report_id: int, approve: bool) -> dict:
        with self._lock:
            entry = next((r for r in self.reports if r["report_id"] == report_id), None)
            if entry is None:
                raise ValueError("Unknown report ID.")
            if entry["status"] != "pending":
                raise ValueError("Only pending reports can be reviewed.")
            entry["status"] = "accepted" if approve else "rejected"
            entry["accepted"] = approve
            entry["reviewed_by"] = "demo_officer"
            if approve:
                self.blocked_roads.add(entry["road_id"])
            self.last_report = entry
            self.version += 1
            result = self._snapshot()
            result["report_result"] = deepcopy(entry)
            return result

    def set_capacity(self, shelter_id: str, capacity_remaining: int) -> dict:
        if shelter_id not in SHELTERS:
            raise ValueError("Unknown demo shelter ID.")
        with self._lock:
            self.shelter_capacity[shelter_id] = capacity_remaining
            self.version += 1
            return self._snapshot()


demo_scenario = DemoScenario()
