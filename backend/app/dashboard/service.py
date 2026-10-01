from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    IncidentRecord,
    IncidentReportRecord,
    NetworkMeta,
    RoadEdgeRecord,
    RoadNodeRecord,
)
from app.road_network.schemas import RouteRequest
from app.road_network.service import NetworkNotFoundError, NoRouteError, find_route
from app.services.demo_scenario import demo_scenario

from .schemas import (
    CitizenDashboard,
    DashboardAlert,
    DashboardRoute,
    DashboardShelter,
    PendingReport,
    PriorityIncident,
    ResponseDashboard,
)


_SEVERITY_RANK = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def _incident_alert(incident: IncidentRecord, *, source: str) -> DashboardAlert:
    return DashboardAlert(
        id=f"incident-{incident.id}",
        title=incident.title,
        category=incident.category,
        severity=incident.severity,
        status=incident.status,
        verification_status=incident.verification_status,
        message=incident.description,
        latitude=incident.latitude,
        longitude=incident.longitude,
        source=source,
        created_at=incident.created_at,
    )


def _network_route(
    session: Session, origin_node_id: str | None
) -> tuple[DashboardRoute, list[DashboardShelter]] | None:
    if not origin_node_id:
        return None

    nodes = session.scalars(select(RoadNodeRecord).order_by(RoadNodeRecord.node_id)).all()
    if not nodes:
        return None

    node_map = {node.node_id: node for node in nodes}
    if origin_node_id not in node_map:
        raise NetworkNotFoundError("Origin node not found.")

    shelters: list[DashboardShelter] = []
    candidates: list[tuple[float, DashboardRoute]] = []
    for node in nodes:
        if node.node_type != "shelter":
            continue
        raw_capacity = (node.properties or {}).get("capacity_remaining")
        capacity = int(raw_capacity) if isinstance(raw_capacity, (int, float)) else None
        availability = (
            "unknown"
            if capacity is None
            else "full" if capacity == 0 else "limited" if capacity < 25 else "available"
        )
        shelters.append(
            DashboardShelter(
                id=node.node_id,
                name=node.label,
                capacity_remaining=capacity,
                availability=availability,
                source="network",
            )
        )
        if capacity == 0:
            continue
        try:
            route = find_route(
                session,
                RouteRequest(
                    origin_node_id=origin_node_id,
                    destination_node_id=node.node_id,
                ),
            )
        except NoRouteError:
            continue
        candidates.append(
            (
                route.weighted_cost,
                DashboardRoute(
                    available=True,
                    destination_id=node.node_id,
                    destination_name=node.label,
                    path_nodes=route.path_nodes,
                    path_edges=route.path_edges,
                    travel_minutes=route.travel_minutes,
                    route_risk=route.route_risk,
                    weighted_cost=route.weighted_cost,
                    warnings=route.warnings,
                    source="network",
                ),
            )
        )

    if candidates:
        return min(candidates, key=lambda item: item[0])[1], shelters

    return (
        DashboardRoute(
            available=False,
            warnings=["No viable route to a currently available shelter."],
            source="network",
        ),
        shelters,
    )


def _simulation_dashboard() -> tuple[DashboardRoute, list[DashboardShelter], str, str, float | None, int]:
    snapshot = demo_scenario.snapshot()
    citizen = snapshot["citizen"]
    route = DashboardRoute(
        available=citizen["route_status"] == "available",
        destination_id=citizen.get("recommended_shelter"),
        destination_name=citizen.get("recommended_shelter"),
        path_nodes=list(citizen.get("route", [])),
        travel_minutes=citizen.get("travel_minutes"),
        route_risk=citizen.get("route_risk"),
        weighted_cost=None,
        warnings=[citizen["message"]],
        source="simulation",
    )
    shelters = []
    for shelter in snapshot["shelters"]:
        capacity = shelter["capacity_remaining"]
        availability = "full" if capacity == 0 else "limited" if capacity < 25 else "available"
        shelters.append(
            DashboardShelter(
                id=shelter["id"],
                name=shelter["name"],
                capacity_remaining=capacity,
                availability=availability,
                source="simulation",
            )
        )
    return (
        route,
        shelters,
        citizen["location"],
        citizen["risk"],
        citizen.get("time_to_isolation_minutes"),
        snapshot["version"],
    )


def build_citizen_dashboard(
    session: Session,
    *,
    origin_node_id: str | None = None,
) -> CitizenDashboard:
    alerts = [
        _incident_alert(incident, source="incident")
        for incident in session.scalars(
            select(IncidentRecord)
            .where(
                IncidentRecord.status == "active",
                IncidentRecord.verification_status == "verified",
            )
            .order_by(IncidentRecord.created_at.desc())
            .limit(20)
        ).all()
    ]

    network_result = _network_route(session, origin_node_id)
    if network_result is not None:
        route, shelters = network_result
        origin_label = session.get(RoadNodeRecord, origin_node_id).label
        meta = session.get(NetworkMeta, 1)
        return CitizenDashboard(
            mode="network",
            notice="Network-backed route and shelter data. Hazard alerts only include verified active incidents.",
            location=origin_label,
            risk="unknown",
            time_to_isolation_minutes=None,
            alerts=alerts,
            shelters=shelters,
            route=route,
            version=meta.version if meta else 0,
        )

    route, shelters, location, risk, tti, version = _simulation_dashboard()
    snapshot = demo_scenario.snapshot()
    if "B12" in snapshot["blocked_roads"]:
        alerts.insert(
            0,
            DashboardAlert(
                id="demo-B12",
                title="Bridge B12 blocked",
                category="blocked_way",
                severity="high",
                status="active",
                verification_status="verified",
                message="Synthetic responder report accepted; route has been recalculated.",
                source="simulation",
            ),
        )

    return CitizenDashboard(
        mode="simulation",
        notice="Synthetic Bihar-style demo only. Do not present this endpoint as live official data.",
        location=location,
        risk=risk,
        time_to_isolation_minutes=tti,
        alerts=alerts,
        shelters=shelters,
        route=route,
        version=version,
    )


def build_response_dashboard(session: Session) -> ResponseDashboard:
    incidents = session.scalars(
        select(IncidentRecord).order_by(IncidentRecord.created_at.desc()).limit(100)
    ).all()
    active = [incident for incident in incidents if incident.status == "active"]
    high_priority = [
        incident for incident in active if _SEVERITY_RANK.get(incident.severity, 0) >= 3
    ]

    priority_rows: list[PriorityIncident] = []
    for incident in sorted(
        active,
        key=lambda item: (_SEVERITY_RANK.get(item.severity, 0), item.created_at),
        reverse=True,
    )[:20]:
        report_count = session.scalar(
            select(func.count(IncidentReportRecord.id)).where(
                IncidentReportRecord.incident_id == incident.id
            )
        ) or 0
        priority_rows.append(
            PriorityIncident(
                id=incident.id,
                title=incident.title,
                category=incident.category,
                severity=incident.severity,
                status=incident.status,
                verification_status=incident.verification_status,
                latitude=incident.latitude,
                longitude=incident.longitude,
                created_at=incident.created_at,
                report_count=int(report_count),
            )
        )

    pending = session.scalars(
        select(IncidentReportRecord)
        .where(IncidentReportRecord.verification_status == "pending")
        .order_by(IncidentReportRecord.created_at.asc())
        .limit(50)
    ).all()
    pending_queue = [
        PendingReport(
            id=report.id,
            incident_id=report.incident_id,
            reporter_role=report.reporter_role,
            confidence=report.confidence,
            created_at=report.created_at,
        )
        for report in pending
    ]

    blocked = set(
        session.scalars(
            select(RoadEdgeRecord.edge_id).where(RoadEdgeRecord.status == "blocked")
        ).all()
    )
    snapshot = demo_scenario.snapshot()
    blocked.update(snapshot["blocked_roads"])
    meta = session.get(NetworkMeta, 1)
    network_rows = session.scalar(select(func.count(RoadEdgeRecord.edge_id))) or 0
    mode = "network" if network_rows else "simulation"

    return ResponseDashboard(
        mode=mode,
        notice=(
            "Network-backed operational view."
            if mode == "network"
            else "Synthetic Bihar-style demo view; operational counts are not live deployments."
        ),
        active_incidents=len(active),
        high_priority_incidents=len(high_priority),
        pending_reports=len(pending_queue),
        blocked_roads=sorted(blocked),
        network_version=meta.version if meta else 0,
        priority_incidents=priority_rows,
        pending_report_queue=pending_queue,
        version=snapshot["version"],
    )
