from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.events.service import emit_notification
from app.models import AuditEventRecord, IncidentRecord, IncidentRoadLinkRecord, NetworkMeta, RoadEdgeRecord, utcnow
from app.road_network.schemas import RouteRequest, RouteResponse
from app.road_network.service import NoRouteError, find_route

from .road_control_schemas import RoadClosureRequest, RoadClosureResponse


class IncidentRoadLinkError(ValueError):
    pass


def _bump_network_version(session: Session) -> int:
    meta = session.get(NetworkMeta, 1)
    if meta is None:
        meta = NetworkMeta(id=1, version=0)
        session.add(meta)
        session.flush()
    meta.version += 1
    session.flush()
    return meta.version


def _route_after_change(
    session: Session, payload: RoadClosureRequest
) -> tuple[bool, RouteResponse | None]:
    if not payload.origin_node_id or not payload.destination_node_id:
        return False, None
    try:
        return True, find_route(
            session,
            RouteRequest(
                origin_node_id=payload.origin_node_id,
                destination_node_id=payload.destination_node_id,
            ),
        )
    except NoRouteError:
        return True, None


def close_incident_road(
    session: Session,
    incident_id: int,
    payload: RoadClosureRequest,
    *,
    actor_user_id: int,
) -> RoadClosureResponse:
    incident = session.get(IncidentRecord, incident_id)
    if incident is None:
        raise IncidentRoadLinkError("Incident not found.")
    if incident.status != "active" or incident.verification_status != "verified":
        raise IncidentRoadLinkError("Only verified active incidents can close a road.")

    edge = session.get(RoadEdgeRecord, payload.edge_id)
    if edge is None:
        raise IncidentRoadLinkError("Road edge not found.")

    active_link = session.scalar(
        select(IncidentRoadLinkRecord)
        .where(
            IncidentRoadLinkRecord.incident_id == incident_id,
            IncidentRoadLinkRecord.edge_id == payload.edge_id,
            IncidentRoadLinkRecord.status == "closed",
        )
        .order_by(IncidentRoadLinkRecord.id.desc())
    )
    if active_link is not None:
        route_available, route = _route_after_change(session, payload)
        meta = session.get(NetworkMeta, 1)
        return RoadClosureResponse(
            incident_id=incident_id,
            edge_id=payload.edge_id,
            status=edge.status,
            network_version=meta.version if meta else 0,
            action="already_closed",
            message="Road is already closed for this incident.",
            rerouted=route_available,
            route=route,
        )

    edge.status = "blocked"
    edge.current_risk = 1.0
    edge.updated_by_user_id = actor_user_id

    link = IncidentRoadLinkRecord(
        incident_id=incident_id,
        edge_id=edge.edge_id,
        status="closed",
        reason=payload.reason,
        created_by_user_id=actor_user_id,
        created_at=utcnow(),
    )
    session.add(link)
    version = _bump_network_version(session)
    session.add(
        AuditEventRecord(
            entity_type="incident",
            entity_id=incident.id,
            action="road_closed_from_incident",
            actor_type="response_team",
            actor_user_id=actor_user_id,
            payload={
                "edge_id": edge.edge_id,
                "reason": payload.reason,
                "network_version": version,
            },
        )
    )
    route_requested, route = _route_after_change(session, payload)
    emit_notification(
        session,
        event_type="road.closed",
        severity="high",
        title="Road closure updated",
        message=f"{edge.edge_id} is now blocked due to a verified incident.",
        target_role="citizen",
        entity_type="road",
        payload={"edge_id": edge.edge_id, "network_version": version},
    )
    emit_notification(
        session,
        event_type="road.closed",
        severity="high",
        title="Road closure applied",
        message=f"{edge.edge_id} was blocked from incident #{incident.id}.",
        target_role="response_team",
        entity_type="incident",
        entity_id=incident.id,
        payload={"edge_id": edge.edge_id, "network_version": version},
    )
    session.commit()

    return RoadClosureResponse(
        incident_id=incident_id,
        edge_id=edge.edge_id,
        status=edge.status,
        network_version=version,
        action="closed",
        message=(
            "Road closure applied and routing state updated."
            if route is not None
            else "Road closure applied. No alternate route was available for the supplied endpoints."
            if route_requested
            else "Road closure applied. Call the routing endpoint with an origin and destination to recalculate."
        ),
        rerouted=route_requested,
        route=route,
    )


def reopen_incident_road(
    session: Session,
    incident_id: int,
    payload: RoadClosureRequest,
    *,
    actor_user_id: int,
) -> RoadClosureResponse:
    incident = session.get(IncidentRecord, incident_id)
    if incident is None:
        raise IncidentRoadLinkError("Incident not found.")

    edge = session.get(RoadEdgeRecord, payload.edge_id)
    if edge is None:
        raise IncidentRoadLinkError("Road edge not found.")

    link = session.scalar(
        select(IncidentRoadLinkRecord)
        .where(
            IncidentRoadLinkRecord.incident_id == incident_id,
            IncidentRoadLinkRecord.edge_id == payload.edge_id,
            IncidentRoadLinkRecord.status == "closed",
        )
        .order_by(IncidentRoadLinkRecord.id.desc())
    )
    if link is None:
        raise IncidentRoadLinkError("No active incident road closure exists.")

    link.status = "reopened"
    link.resolved_at = utcnow()
    edge.status = "open"
    edge.current_risk = edge.base_risk
    edge.updated_by_user_id = actor_user_id
    version = _bump_network_version(session)
    session.add(
        AuditEventRecord(
            entity_type="incident",
            entity_id=incident.id,
            action="road_reopened_from_incident",
            actor_type="response_team",
            actor_user_id=actor_user_id,
            payload={"edge_id": edge.edge_id, "network_version": version},
        )
    )
    route_requested, route = _route_after_change(session, payload)
    emit_notification(
        session,
        event_type="road.reopened",
        severity="medium",
        title="Road reopened",
        message=f"{edge.edge_id} has been reopened.",
        target_role="citizen",
        entity_type="road",
        payload={"edge_id": edge.edge_id, "network_version": version},
    )
    session.commit()

    return RoadClosureResponse(
        incident_id=incident_id,
        edge_id=edge.edge_id,
        status=edge.status,
        network_version=version,
        action="reopened",
        message="Road reopened and routing state updated.",
        rerouted=route_requested,
        route=route,
    )
