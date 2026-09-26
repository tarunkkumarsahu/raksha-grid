"""Synthetic disaster scenario used by the RAKSHA Grid integration demo.

The routing and intelligence calculations are deterministic demo logic. Mutable
scenario facts are persisted in SQL via ScenarioStateStore so application
restarts do not silently erase road closures, reports, or shelter capacity.

This is NOT a real evacuation or flood forecast.
"""
from copy import deepcopy
from threading import RLock

import networkx as nx

from app.database import init_db
from app.schemas import GroundReportInput, RouteEdge, SafeCorridorRequest, SettlementInput
from app.services.ground_intel import score_ground_report
from app.services.isolation import compute_isolation_intelligence
from app.services.routing import find_safe_corridor
from app.services.state_store import ScenarioState, ScenarioStateStore


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
SHELTERS = {
    "Shelter_A": {"name": "Shelter A", "capacity": 50},
    "Shelter_B": {"name": "Shelter B", "capacity": 120},
}


class DemoScenario:
    def __init__(self, store: ScenarioStateStore | None = None) -> None:
        self._lock = RLock()
        if store is None:
            init_db()
            self._store = ScenarioStateStore()
        else:
            self._store = store
        self._store.ensure_seeded(
            road_ids=list(ROADS),
            shelter_defaults=self._default_shelter_capacity(),
        )

    @staticmethod
    def _default_shelter_capacity() -> dict[str, int]:
        return {key: value["capacity"] for key, value in SHELTERS.items()}

    def reset(self) -> dict:
        with self._lock:
            state = self._store.reset(
                road_ids=list(ROADS),
                shelter_defaults=self._default_shelter_capacity(),
            )
            return self._snapshot(state)

    def _edges(self, state: ScenarioState) -> list[RouteEdge]:
        return [
            RouteEdge(
                source=a,
                target=b,
                travel_minutes=t,
                hazard_risk=r,
                blocked=road_id in state.blocked_roads,
            )
            for road_id, (a, b, t, r, _failure) in ROADS.items()
        ]

    def _graph(self, state: ScenarioState) -> nx.Graph:
        graph = nx.Graph()
        for road_id, (a, b, travel, risk, failure) in ROADS.items():
            if road_id not in state.blocked_roads:
                graph.add_edge(
                    a,
                    b,
                    id=road_id,
                    time=travel,
                    risk=risk,
                    failure=failure,
                )
        return graph

    def _routes(self, origin: str, state: ScenarioState) -> list[dict]:
        candidates = []
        for shelter_id, remaining in state.shelter_capacity.items():
            if remaining < SETTLEMENTS[origin]["evacuees"]:
                continue
            try:
                route = find_safe_corridor(
                    SafeCorridorRequest(
                        origin=origin,
                        destination=shelter_id,
                        edges=self._edges(state),
                    )
                )
                candidates.append(
                    {
                        "shelter_id": shelter_id,
                        "name": SHELTERS[shelter_id]["name"],
                        **route.model_dump(),
                    }
                )
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
        return sorted(candidates, key=lambda candidate: candidate["weighted_cost"])

    def _access(self, origin: str, state: ScenarioState) -> tuple[int, float]:
        graph = self._graph(state)
        shelters = [
            shelter_id
            for shelter_id in SHELTERS
            if state.shelter_capacity.get(shelter_id, 0)
            >= SETTLEMENTS[origin]["evacuees"]
        ]
        failures = []
        if origin not in graph:
            return 0, 0.0

        for neighbor in graph.neighbors(origin):
            trial = graph.copy()
            trial.remove_node(origin)
            if neighbor in trial and any(
                shelter in trial and nx.has_path(trial, neighbor, shelter)
                for shelter in shelters
            ):
                failures.append(graph[origin][neighbor]["failure"])

        return len(failures), float(max(failures)) if failures else 0.0

    def _settlement(self, origin: str, state: ScenarioState) -> dict:
        info = SETTLEMENTS[origin]
        exits, last_exit_minutes = self._access(origin, state)
        routes = self._routes(origin, state)

        # Failure horizons remain synthetic scenario inputs, not ML predictions.
        risk = compute_isolation_intelligence(
            SettlementInput(
                id="DEMO-" + origin.upper(),
                name=origin,
                population=info["population"],
                vulnerable_population=info["vulnerable"],
                flood_risk=info["flood_risk"],
                route_risk=0.65 if exits <= 1 else 0.28,
                medical_urgency=0.25,
                shelter_accessibility=0.75 if routes else 0.0,
                predicted_exit_failure_minutes=[last_exit_minutes] * exits,
                data_mode="simulation",
            )
        )
        chosen = routes[0] if routes else None

        return {
            "settlement": origin,
            "population_exposed": info["population"],
            "people_to_evacuate_demo": info["evacuees"],
            "safe_exits_remaining": exits,
            "time_to_isolation_minutes": last_exit_minutes,
            "priority_score": risk.priority_score,
            "priority_band": risk.priority_band,
            "explanation": risk.explanation,
            "recommended_shelter": chosen["name"] if chosen else "No reachable shelter",
            "shelter_id": chosen["shelter_id"] if chosen else None,
            "route": chosen["path"] if chosen else [],
            "travel_minutes": chosen["travel_minutes"] if chosen else None,
            "route_risk": chosen["route_risk"] if chosen else None,
            "route_status": "available" if chosen else "unavailable",
        }

    def _snapshot(self, state: ScenarioState) -> dict:
        villages = {
            name: self._settlement(name, state)
            for name in SETTLEMENTS
        }
        rampur = villages["Rampur"]
        ordered = sorted(
            villages.values(),
            key=lambda village: village["priority_score"],
            reverse=True,
        )

        if rampur["route_status"] == "unavailable":
            citizen_message = (
                "NO VERIFIED EVACUATION ROUTE. Contact local emergency services "
                "and follow official advice."
            )
        elif state.blocked_roads:
            citizen_message = (
                "Route recalculated after a reported road closure. "
                "Seek official confirmation."
            )
        else:
            citizen_message = (
                "A modelled evacuation route is available. Check official instructions."
            )

        return deepcopy(
            {
                "mode": "simulation",
                "notice": (
                    "ALL locations, reports, capacities and predicted times are synthetic; "
                    "route is NOT certified safe."
                ),
                "storage": "persistent_sql",
                "version": state.version,
                "event": "Round-1 demo - synthetic flood scenario",
                "blocked_roads": sorted(state.blocked_roads),
                "roads": [
                    {
                        "id": road_id,
                        "source": values[0],
                        "target": values[1],
                        "blocked": road_id in state.blocked_roads,
                    }
                    for road_id, values in ROADS.items()
                ],
                "shelters": [
                    {
                        "id": shelter_id,
                        "name": SHELTERS[shelter_id]["name"],
                        "capacity_remaining": capacity,
                    }
                    for shelter_id, capacity in state.shelter_capacity.items()
                ],
                "settlements": villages,
                "last_report": state.last_report,
                "reports": state.reports,
                "citizen": {
                    "location": "Rampur",
                    "risk": rampur["priority_band"],
                    "time_to_isolation_minutes": rampur["time_to_isolation_minutes"],
                    "recommended_shelter": rampur["recommended_shelter"],
                    "route": rampur["route"],
                    "travel_minutes": rampur["travel_minutes"],
                    "route_risk": rampur["route_risk"],
                    "route_status": rampur["route_status"],
                    "message": citizen_message,
                },
                "responder": {
                    "mission": "Rampur evacuation support",
                    "priority": rampur["priority_band"],
                    "population_exposed": rampur["population_exposed"],
                    "safe_exits_remaining": rampur["safe_exits_remaining"],
                    "approach_route": rampur["route"],
                    "message": (
                        "No usable route in the model. Do NOT proceed without official direction."
                        if rampur["route_status"] == "unavailable"
                        else "Bridge B12 is blocked. Approach through Road R12."
                        if "B12" in state.blocked_roads
                        else "Check current route and official field status."
                    ),
                },
                "officer": {
                    "settlement": "Rampur",
                    "priority_score": rampur["priority_score"],
                    "priority_band": rampur["priority_band"],
                    "time_to_isolation_minutes": rampur["time_to_isolation_minutes"],
                    "safe_exits_remaining": rampur["safe_exits_remaining"],
                    "recommended_shelter": rampur["recommended_shelter"],
                    "blocked_roads": sorted(state.blocked_roads),
                    "explanation": rampur["explanation"],
                    "priority_settlements": ordered,
                    "pending_reports": [
                        report
                        for report in state.reports
                        if report["status"] == "pending"
                    ],
                },
            }
        )

    def snapshot(self) -> dict:
        with self._lock:
            return self._snapshot(self._store.load())

    def report_blocked_road(
        self,
        road_id: str,
        report: GroundReportInput,
        reason: str = "Flooded / blocked",
    ) -> dict:
        if road_id not in ROADS:
            raise ValueError("Unknown demo road ID.")

        with self._lock:
            score = score_ground_report(report)
            auto_accept = (
                score.state == "actionable"
                and report.reporter_role in {"responder", "officer"}
                and report.contradicting_reports == 0
            )
            pending = not auto_accept and score.confidence >= 0.25
            status = "accepted" if auto_accept else "pending" if pending else "rejected"

            persisted = self._store.record_report(
                {
                    "road_id": road_id,
                    "reason": reason,
                    "confidence": score.confidence,
                    "state": score.state,
                    "accepted": auto_accept,
                    "status": status,
                    "evidence": score.evidence,
                },
                block_road=auto_accept,
            )

            result = self._snapshot(self._store.load())
            result["report_result"] = persisted
            return result

    def review_report(self, report_id: int, approve: bool) -> dict:
        with self._lock:
            persisted = self._store.review_report(report_id, approve)
            result = self._snapshot(self._store.load())
            result["report_result"] = persisted
            return result

    def set_capacity(self, shelter_id: str, capacity_remaining: int) -> dict:
        if shelter_id not in SHELTERS:
            raise ValueError("Unknown demo shelter ID.")

        with self._lock:
            self._store.set_shelter_capacity(shelter_id, capacity_remaining)
            return self._snapshot(self._store.load())


demo_scenario = DemoScenario()
