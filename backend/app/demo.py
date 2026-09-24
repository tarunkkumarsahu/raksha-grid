"""Stateful, explicitly synthetic three-role demo; not an emergency service.

All nodes, people counts, road failure times and shelter capacities are invented
for a transparent hackathon exercise. No real coordinates or verified safe routes.
"""
from datetime import datetime, timezone
from threading import RLock

import networkx as nx
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Literal
from pathlib import Path

from app.schemas import GroundReportInput, RouteEdge, SafeCorridorRequest
from app.services.ground_intel import score_ground_report
from app.services.routing import find_safe_corridor

router = APIRouter(prefix="/demo", tags=["Demo: SIMULATION ONLY"])
_LOCK = RLock()

NODES = {
    "rampur": {"name": "Rampur (fictional)", "x": 12, "y": 48},
    "bridge": {"name": "Bridge junction", "x": 43, "y": 24},
    "crossroad": {"name": "Crossroad", "x": 43, "y": 74},
    "shelter-a": {"name": "Shelter A", "x": 82, "y": 24},
    "shelter-b": {"name": "Shelter B", "x": 82, "y": 74},
    "basantpur": {"name": "Basantpur (fictional)", "x": 68, "y": 8},
}
ROADS = [
    {"id": "BR-12", "source": "rampur", "target": "bridge", "travel_minutes": 7.0,
     "hazard_risk": 0.07, "failure_in_minutes": 37.0},
    {"id": "R-12A", "source": "bridge", "target": "shelter-a", "travel_minutes": 5.0,
     "hazard_risk": 0.05, "failure_in_minutes": None},
    {"id": "R-08", "source": "rampur", "target": "crossroad", "travel_minutes": 7.0,
     "hazard_risk": 0.22, "failure_in_minutes": 21.0},
    {"id": "R-08B", "source": "crossroad", "target": "shelter-b", "travel_minutes": 9.0,
     "hazard_risk": 0.09, "failure_in_minutes": None},
    {"id": "R-21", "source": "basantpur", "target": "shelter-a", "travel_minutes": 9.0,
     "hazard_risk": 0.08, "failure_in_minutes": None},
]
SHELTERS = [
    {"id": "shelter-a", "name": "Shelter A", "capacity_remaining": 300},
    {"id": "shelter-b", "name": "Shelter B", "capacity_remaining": 220},
]
SETTLEMENTS = [
    {"id": "rampur", "name": "Rampur (fictional)", "population": 1840,
     "people_needing_shelter": 80, "vulnerable_people": 510, "flood_exposure": 0.88},
    {"id": "basantpur", "name": "Basantpur (fictional)", "population": 4200,
     "people_needing_shelter": 75, "vulnerable_people": 760, "flood_exposure": 0.58},
]


def _new_state(version=1):
    return {"version": version, "blocked": set(), "reports": [], "events": [
        {"message": "Synthetic flood scenario started. No roads are confirmed closed.",
         "time": datetime.now(timezone.utc).isoformat()}]}


_STATE = _new_state()


class SubmitReport(BaseModel):
    road_id: str
    reporter_role: Literal["citizen", "responder"]
    observation: Literal["road_flooded", "bridge_submerged", "road_clear"]
    note: str = Field(default="", max_length=250)


class ReviewReport(BaseModel):
    # A demo-only role selector: NO authentication/authorization is implemented.
    reviewer_role: Literal["officer"]
    decision: Literal["confirm_blocked", "reject_report"]


def _road_graph(blocked, at_minutes=0.0):
    g = nx.Graph()
    g.add_nodes_from(NODES)
    for road in ROADS:
        if road["id"] in blocked:
            continue
        failure = road["failure_in_minutes"]
        if failure is not None and failure <= at_minutes:
            continue
        g.add_edge(road["source"], road["target"], **road)
    return g


def _reachable_shelters(graph, origin):
    return [s for s in SHELTERS
            if s["capacity_remaining"] > 0 and nx.has_path(graph, origin, s["id"])]


def _time_to_isolation(origin, blocked):
    """Simplified graph failure simulation, not a hydrological forecast."""
    g = _road_graph(blocked)
    if not _reachable_shelters(g, origin):
        return 0.0

    deadlines = sorted({r["failure_in_minutes"] for r in ROADS
                        if r["id"] not in blocked and r["failure_in_minutes"] is not None})
    for t in deadlines:
        if not _reachable_shelters(_road_graph(blocked, t), origin):
            return t
    return None  # At least one route still exists after all modelled failures.


def _exit_count(origin, blocked):
    graph = _road_graph(blocked)
    total = 0
    for neighbour in graph.neighbors(origin):
        subgraph = graph.copy()
        subgraph.remove_node(origin)
        if _reachable_shelters(subgraph, neighbour):
            total += 1
    return total


def _routes_for(origin, blocked):
    active_roads = [
        RouteEdge(source=r["source"], target=r["target"],
                  travel_minutes=r["travel_minutes"], hazard_risk=r["hazard_risk"])
        for r in ROADS if r["id"] not in blocked
    ]
    routes = []
    for shelter in SHELTERS:
        if shelter["capacity_remaining"] <= 0:
            continue
        try:
            result = find_safe_corridor(SafeCorridorRequest(
                origin=origin, destination=shelter["id"], edges=active_roads))
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
        routes.append({
            "shelter_id": shelter["id"], "shelter_name": shelter["name"],
            "available_places": shelter["capacity_remaining"],
            "path": result.path,
            "path_labels": [NODES[n]["name"] for n in result.path],
            "travel_minutes": result.travel_minutes,
            "route_risk_index": result.route_risk,
            "weighted_cost": result.weighted_cost,
            "status": "PROVISIONAL - simulation only",
        })
    return sorted(routes, key=lambda r: r["weighted_cost"])


def _settlement_status(item, blocked):
    tti = _time_to_isolation(item["id"], blocked)
    exits = _exit_count(item["id"], blocked)
    vulnerability = item["vulnerable_people"] / item["population"]
    urgency = (1.0 if tti == 0 else
               max(0.0, (90.0 - tti) / 90.0) if tti is not None else 0.0)
    score = round(100 * (
        0.34 * urgency + 0.26 * (1.0 if exits == 0 else 1.0 / exits)
        + 0.25 * item["flood_exposure"] + 0.15 * vulnerability), 1)
    routes = _routes_for(item["id"], blocked)
    reasons = [
        "No reachable shelter remains." if exits == 0 else f"{exits} usable exit(s) remain.",
        ("No isolation time can be estimated from the available scenario failures."
         if tti is None else f"Last route fails at simulated minute {tti:g}."),
        "Rank is a deterministic demo score, not a validated hazard prediction."
    ]
    return {**item, "usable_exits": exits, "time_to_isolation_minutes": tti,
            "priority_score": score, "explanation": reasons,
            "recommended_route": routes[0] if routes else None,
            "alternative_routes": routes[1:], "is_isolated": not routes}


def _snapshot():
    blocked = set(_STATE["blocked"])
    settlements = [_settlement_status(item, blocked) for item in SETTLEMENTS]
    settlements.sort(key=lambda s: s["priority_score"], reverse=True)
    return {
        "mode": "simulation",
        "notice": ("All place names, road links, capacities, population, flood exposure and "
                   "failure-time inputs here are fictional. This is NOT a live emergency tool."),
        "version": _STATE["version"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nodes": [{**v, "id": k} for k, v in NODES.items()],
        "roads": [{**road, "blocked": road["id"] in blocked} for road in ROADS],
        "shelters": SHELTERS,
        "priority_settlements": settlements,
        "reports": [dict(r) for r in _STATE["reports"]],
        "events": list(_STATE["events"][-8:]),
    }


@router.get("/state")
def demo_state():
    with _LOCK:
        return _snapshot()


@router.post("/reports", status_code=201)
def submit_report(payload: SubmitReport):
    with _LOCK:
        if not any(road["id"] == payload.road_id for road in ROADS):
            raise HTTPException(status_code=404, detail="Unknown simulated road.")
        report_id = f"REP-{len(_STATE['reports']) + 1:04d}"
        confidence = score_ground_report(
            GroundReportInput(reporter_role=payload.reporter_role))
        report = {
            "id": report_id, **payload.model_dump(),
            "confidence": confidence.confidence,
            "status": "pending_officer_review",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }
        _STATE["reports"].append(report)
        _STATE["version"] += 1
        _STATE["events"].append({"message": f"{report_id}: {payload.road_id} reported; awaiting officer review.",
                                 "time": report["submitted_at"]})
        return {"report": report, "state": _snapshot()}


@router.post("/reports/{report_id}/review")
def review_report(report_id: str, payload: ReviewReport):
    with _LOCK:
        report = next((r for r in _STATE["reports"] if r["id"] == report_id), None)
        if report is None:
            raise HTTPException(status_code=404, detail="Report not found.")
        if report["status"] != "pending_officer_review":
            raise HTTPException(status_code=409, detail="Report already reviewed.")
        report["status"] = ("confirmed_blocked" if payload.decision == "confirm_blocked"
                            else "rejected")
        if payload.decision == "confirm_blocked":
            _STATE["blocked"].add(report["road_id"])
        _STATE["version"] += 1
        _STATE["events"].append({
            "message": (f"{report_id} reviewed: {report['road_id']} "
                        f"{'BLOCKED; routes recalculated.' if payload.decision == 'confirm_blocked' else 'report rejected.'}"),
            "time": datetime.now(timezone.utc).isoformat(),
        })
        return {"report": dict(report), "state": _snapshot()}


@router.post("/reset")
def reset_demo():
    global _STATE
    with _LOCK:
        _STATE = _new_state(_STATE["version"] + 1)
        return _snapshot()


@router.get("/ui", response_class=HTMLResponse, include_in_schema=False)
def demo_ui():
    return (Path(__file__).parent / "demo_ui.html").read_text(encoding="utf-8")
