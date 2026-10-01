from __future__ import annotations

import math

import networkx as nx
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import NetworkMeta, RoadEdgeRecord, RoadNodeRecord

from .schemas import (
    NetworkImportRequest,
    NetworkSnapshot,
    RoadEdgeRead,
    RoadEdgeStatusUpdate,
    RoadNodeRead,
    RouteRequest,
    RouteResponse,
)


RISK_WEIGHT = 2.5
RESTRICTED_PENALTY = 1.35


class NetworkNotFoundError(ValueError):
    pass


class NetworkValidationError(ValueError):
    pass


class NoRouteError(ValueError):
    pass


def _meta(session: Session, *, create: bool) -> NetworkMeta | None:
    meta = session.get(NetworkMeta, 1)
    if meta is None and create:
        meta = NetworkMeta(id=1, version=0)
        session.add(meta)
        session.flush()
    return meta


def _bump_version(session: Session) -> int:
    meta = _meta(session, create=True)
    assert meta is not None
    meta.version += 1
    session.flush()
    return meta.version


def _node_read(row: RoadNodeRecord) -> RoadNodeRead:
    return RoadNodeRead(
        node_id=row.node_id,
        label=row.label,
        node_type=row.node_type,
        latitude=row.latitude,
        longitude=row.longitude,
        external_ref=row.external_ref,
        properties=dict(row.properties or {}),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _edge_read(row: RoadEdgeRecord) -> RoadEdgeRead:
    return RoadEdgeRead(
        edge_id=row.edge_id,
        source_node_id=row.source_node_id,
        target_node_id=row.target_node_id,
        bidirectional=row.bidirectional,
        travel_minutes=row.travel_minutes,
        distance_meters=row.distance_meters,
        base_risk=row.base_risk,
        current_risk=row.current_risk,
        status=row.status,
        failure_horizon_minutes=row.failure_horizon_minutes,
        external_ref=row.external_ref,
        geometry_geojson=row.geometry_geojson,
        updated_by_user_id=row.updated_by_user_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def get_network_snapshot(session: Session) -> NetworkSnapshot:
    meta = _meta(session, create=False)
    nodes = session.scalars(select(RoadNodeRecord).order_by(RoadNodeRecord.node_id)).all()
    edges = session.scalars(select(RoadEdgeRecord).order_by(RoadEdgeRecord.edge_id)).all()
    return NetworkSnapshot(
        version=meta.version if meta else 0,
        nodes=[_node_read(row) for row in nodes],
        edges=[_edge_read(row) for row in edges],
    )


def import_network(
    session: Session,
    payload: NetworkImportRequest,
    *,
    actor_user_id: int,
) -> NetworkSnapshot:
    node_ids = [node.node_id for node in payload.nodes]
    edge_ids = [edge.edge_id for edge in payload.edges]
    if len(node_ids) != len(set(node_ids)):
        raise NetworkValidationError("Duplicate node IDs in network import.")
    if len(edge_ids) != len(set(edge_ids)):
        raise NetworkValidationError("Duplicate edge IDs in network import.")

    try:
        if payload.replace_existing:
            session.execute(delete(RoadEdgeRecord))
            session.execute(delete(RoadNodeRecord))
            existing_node_ids: set[str] = set()
        else:
            existing_node_ids = set(session.scalars(select(RoadNodeRecord.node_id)).all())

        allowed_node_ids = existing_node_ids | set(node_ids)
        for edge in payload.edges:
            if edge.source_node_id not in allowed_node_ids or edge.target_node_id not in allowed_node_ids:
                raise NetworkValidationError(
                    f"Edge {edge.edge_id} references an unknown node."
                )

        for node in payload.nodes:
            row = session.get(RoadNodeRecord, node.node_id)
            if row is None:
                row = RoadNodeRecord(node_id=node.node_id)
                session.add(row)
            row.label = node.label
            row.node_type = node.node_type
            row.latitude = node.latitude
            row.longitude = node.longitude
            row.external_ref = node.external_ref
            row.properties = dict(node.properties)

        session.flush()

        for edge in payload.edges:
            row = session.get(RoadEdgeRecord, edge.edge_id)
            if row is None:
                row = RoadEdgeRecord(edge_id=edge.edge_id)
                session.add(row)
            row.source_node_id = edge.source_node_id
            row.target_node_id = edge.target_node_id
            row.bidirectional = edge.bidirectional
            row.travel_minutes = edge.travel_minutes
            row.distance_meters = edge.distance_meters
            row.base_risk = edge.base_risk
            row.current_risk = (
                edge.current_risk if edge.current_risk is not None else edge.base_risk
            )
            row.status = edge.status
            row.failure_horizon_minutes = edge.failure_horizon_minutes
            row.external_ref = edge.external_ref
            row.geometry_geojson = edge.geometry_geojson
            row.updated_by_user_id = actor_user_id

        _bump_version(session)
        session.commit()
    except Exception:
        session.rollback()
        raise

    return get_network_snapshot(session)


def update_edge_status(
    session: Session,
    edge_id: str,
    payload: RoadEdgeStatusUpdate,
    *,
    actor_user_id: int,
) -> RoadEdgeRead:
    edge = session.get(RoadEdgeRecord, edge_id)
    if edge is None:
        raise NetworkNotFoundError("Road edge not found.")

    edge.status = payload.status
    if payload.current_risk is not None:
        edge.current_risk = payload.current_risk
    edge.failure_horizon_minutes = payload.failure_horizon_minutes
    edge.updated_by_user_id = actor_user_id
    _bump_version(session)
    session.commit()
    return _edge_read(edge)


def _edge_cost(edge: RoadEdgeRecord) -> float:
    risk = max(edge.base_risk, edge.current_risk)
    penalty = RESTRICTED_PENALTY if edge.status == "restricted" else 1.0
    return edge.travel_minutes * (1.0 + RISK_WEIGHT * risk) * penalty


def find_route(session: Session, payload: RouteRequest) -> RouteResponse:
    node_ids = set(session.scalars(select(RoadNodeRecord.node_id)).all())
    if payload.origin_node_id not in node_ids:
        raise NetworkNotFoundError("Origin node not found.")
    if payload.destination_node_id not in node_ids:
        raise NetworkNotFoundError("Destination node not found.")

    graph = nx.MultiDiGraph()
    graph.add_nodes_from(node_ids)

    edges = session.scalars(select(RoadEdgeRecord)).all()
    for edge in edges:
        if edge.status == "blocked":
            continue

        attrs = {
            "edge_id": edge.edge_id,
            "travel_minutes": edge.travel_minutes,
            "risk": max(edge.base_risk, edge.current_risk),
            "status": edge.status,
            "weighted_cost": _edge_cost(edge),
        }
        graph.add_edge(
            edge.source_node_id,
            edge.target_node_id,
            key=edge.edge_id,
            **attrs,
        )
        if edge.bidirectional:
            graph.add_edge(
                edge.target_node_id,
                edge.source_node_id,
                key=edge.edge_id,
                **attrs,
            )

    try:
        path_nodes = nx.shortest_path(
            graph,
            payload.origin_node_id,
            payload.destination_node_id,
            weight="weighted_cost",
        )
    except nx.NetworkXNoPath as exc:
        raise NoRouteError("No viable route exists with the current road status.") from exc

    path_edges: list[str] = []
    travel = 0.0
    weighted = 0.0
    risks: list[float] = []
    warnings: list[str] = []

    for source, target in zip(path_nodes, path_nodes[1:]):
        options = graph.get_edge_data(source, target)
        if not options:
            raise NoRouteError("Route reconstruction failed.")
        edge_key, data = min(
            options.items(),
            key=lambda item: item[1]["weighted_cost"],
        )
        path_edges.append(str(edge_key))
        travel += float(data["travel_minutes"])
        weighted += float(data["weighted_cost"])
        risks.append(float(data["risk"]))
        if data["status"] == "restricted":
            warnings.append(f"Restricted road segment used: {edge_key}.")

    route_risk = 0.0 if not risks else 1.0 - math.prod(1.0 - risk for risk in risks)
    if route_risk >= 0.5:
        warnings.append("Route has elevated cumulative hazard risk.")

    meta = _meta(session, create=False)
    return RouteResponse(
        network_version=meta.version if meta else 0,
        origin_node_id=payload.origin_node_id,
        destination_node_id=payload.destination_node_id,
        path_nodes=path_nodes,
        path_edges=path_edges,
        travel_minutes=round(travel, 1),
        route_risk=round(route_risk, 3),
        weighted_cost=round(weighted, 2),
        warnings=warnings,
    )
