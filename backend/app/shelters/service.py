from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.events.service import emit_notification
from app.models import AuditEventRecord, NetworkMeta, RoadNodeRecord, utcnow
from app.road_network.schemas import RouteRequest, RouteResponse
from app.road_network.service import NoRouteError, NetworkNotFoundError, find_route

from .schemas import (
    ShelterAllocationRequest,
    ShelterAllocationResponse,
    ShelterCandidate,
    ShelterCapacityUpdate,
    ShelterRead,
)


def _bump_version(session: Session) -> int:
    meta = session.get(NetworkMeta, 1)
    if meta is None:
        meta = NetworkMeta(id=1, version=0)
        session.add(meta)
        session.flush()
    meta.version += 1
    session.flush()
    return meta.version


def _shelter_read(node: RoadNodeRecord) -> ShelterRead:
    props = dict(node.properties or {})
    total = props.get("capacity_total")
    remaining = props.get("capacity_remaining")
    occupied = props.get("occupied")
    total_int = int(total) if isinstance(total, (int, float)) else None
    remaining_int = int(remaining) if isinstance(remaining, (int, float)) else None
    occupied_int = int(occupied) if isinstance(occupied, (int, float)) else None
    if remaining_int == 0:
        availability = "full"
    elif remaining_int is not None and remaining_int < 25:
        availability = "limited"
    elif remaining_int is not None:
        availability = "available"
    else:
        availability = "unknown"
    return ShelterRead(
        node_id=node.node_id,
        name=node.label,
        capacity_total=total_int,
        capacity_remaining=remaining_int,
        occupied=occupied_int,
        availability=availability,
        latitude=node.latitude,
        longitude=node.longitude,
    )


def list_shelters(session: Session) -> list[ShelterRead]:
    nodes = session.scalars(
        select(RoadNodeRecord)
        .where(RoadNodeRecord.node_type == "shelter")
        .order_by(RoadNodeRecord.label)
    ).all()
    return [_shelter_read(node) for node in nodes]


def update_shelter_capacity(
    session: Session,
    node_id: str,
    payload: ShelterCapacityUpdate,
    *,
    actor_user_id: int,
) -> ShelterRead:
    node = session.get(RoadNodeRecord, node_id)
    if node is None or node.node_type != "shelter":
        raise NetworkNotFoundError("Shelter node not found.")

    props = dict(node.properties or {})
    previous = props.get("capacity_remaining")
    total = props.get("capacity_total")
    if isinstance(total, (int, float)) and payload.capacity_remaining > int(total):
        raise ValueError("Remaining capacity cannot exceed total capacity.")

    props["capacity_remaining"] = payload.capacity_remaining
    if "capacity_total" not in props:
        props["capacity_total"] = payload.capacity_remaining
    if isinstance(props.get("capacity_total"), (int, float)):
        props["occupied"] = max(
            0,
            int(props["capacity_total"]) - payload.capacity_remaining,
        )
    node.properties = props
    version = _bump_version(session)
    session.add(
        AuditEventRecord(
            entity_type="shelter",
            entity_id=0,
            action="shelter_capacity_updated",
            actor_type="response_team",
            actor_user_id=actor_user_id,
            payload={
                "node_id": node_id,
                "previous_capacity_remaining": previous,
                "capacity_remaining": payload.capacity_remaining,
                "reason": payload.reason,
                "network_version": version,
            },
            created_at=utcnow(),
        )
    )
    if payload.capacity_remaining <= 25:
        emit_notification(
            session,
            event_type="shelter.capacity_low",
            severity="high",
            title=f"{node.label} capacity is low",
            message=f"Only {payload.capacity_remaining} places remain.",
            target_role="citizen",
            entity_type="shelter",
            payload={"node_id": node_id, "capacity_remaining": payload.capacity_remaining},
        )
    emit_notification(
        session,
        event_type="shelter.capacity_updated",
        severity="medium",
        title="Shelter capacity updated",
        message=f"{node.label} capacity is now {payload.capacity_remaining}.",
        target_role="response_team",
        entity_type="shelter",
        payload={"node_id": node_id, "capacity_remaining": payload.capacity_remaining},
    )
    session.commit()
    return _shelter_read(node)


def allocate_shelter(
    session: Session,
    payload: ShelterAllocationRequest,
) -> ShelterAllocationResponse:
    nodes = session.scalars(
        select(RoadNodeRecord)
        .where(RoadNodeRecord.node_type == "shelter")
        .order_by(RoadNodeRecord.node_id)
    ).all()
    if not nodes:
        raise NetworkNotFoundError("No shelter nodes are loaded.")

    candidates: list[ShelterCandidate] = []
    ranked: list[tuple[float, ShelterRead, RouteResponse]] = []
    for node in nodes:
        shelter = _shelter_read(node)
        remaining = shelter.capacity_remaining
        if remaining is None:
            candidates.append(
                ShelterCandidate(
                    shelter=shelter,
                    eligible=False,
                    reason="Shelter capacity is unknown.",
                )
            )
            continue
        if remaining < payload.people_count:
            candidates.append(
                ShelterCandidate(
                    shelter=shelter,
                    eligible=False,
                    reason="Insufficient remaining capacity.",
                )
            )
            continue
        try:
            route = find_route(
                session,
                RouteRequest(
                    origin_node_id=payload.origin_node_id,
                    destination_node_id=node.node_id,
                ),
            )
        except (NoRouteError, NetworkNotFoundError) as exc:
            candidates.append(
                ShelterCandidate(
                    shelter=shelter,
                    eligible=False,
                    reason=str(exc),
                )
            )
            continue
        candidates.append(
            ShelterCandidate(
                shelter=shelter,
                route=route,
                eligible=True,
                reason="Capacity and route are available.",
            )
        )
        ranked.append((route.weighted_cost, shelter, route))

    meta = session.get(NetworkMeta, 1)
    if not ranked:
        return ShelterAllocationResponse(
            origin_node_id=payload.origin_node_id,
            people_count=payload.people_count,
            candidates=candidates,
            network_version=meta.version if meta else 0,
            message="No shelter satisfies both capacity and route constraints.",
        )

    _, selected_shelter, selected_route = min(ranked, key=lambda item: item[0])
    return ShelterAllocationResponse(
        origin_node_id=payload.origin_node_id,
        people_count=payload.people_count,
        selected_shelter=selected_shelter,
        selected_route=selected_route,
        candidates=candidates,
        network_version=meta.version if meta else 0,
        message="Shelter selected using available capacity and current route cost.",
    )
