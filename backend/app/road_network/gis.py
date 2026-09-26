from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy.orm import Session

from .gis_schemas import GeoJSONFeatureCollection
from .schemas import NetworkImportRequest, RoadEdgeInput, RoadNodeInput
from .service import NetworkValidationError, import_network


def _coordinates_point(geometry: dict) -> tuple[float, float]:
    if geometry.get("type") != "Point":
        raise NetworkValidationError("Node feature geometry must be a Point.")
    coordinates = geometry.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) < 2:
        raise NetworkValidationError("Point geometry must contain [longitude, latitude].")
    longitude, latitude = float(coordinates[0]), float(coordinates[1])
    if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
        raise NetworkValidationError("GeoJSON coordinates are outside valid bounds.")
    return longitude, latitude


def _line_coordinates(geometry: dict) -> list[list[float]]:
    if geometry.get("type") != "LineString":
        raise NetworkValidationError("Road feature geometry must be a LineString.")
    coordinates = geometry.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) < 2:
        raise NetworkValidationError("LineString geometry must contain at least two positions.")
    return coordinates


def geojson_to_network(payload: GeoJSONFeatureCollection) -> NetworkImportRequest:
    nodes: list[RoadNodeInput] = []
    edges: list[RoadEdgeInput] = []

    for feature in payload.features:
        props = dict(feature.properties or {})
        geometry = dict(feature.geometry or {})
        geometry_type = geometry.get("type")

        if geometry_type == "Point":
            node_id = props.get("node_id")
            if not node_id:
                raise NetworkValidationError("Point feature is missing properties.node_id.")
            longitude, latitude = _coordinates_point(geometry)
            node_type = props.get("node_type", "other")
            if node_type not in {"junction", "settlement", "shelter", "hospital", "bridge", "other"}:
                raise NetworkValidationError(f"Unsupported node_type: {node_type}")
            reserved = {"node_id", "label", "node_type", "external_ref"}
            extra = {key: value for key, value in props.items() if key not in reserved}
            nodes.append(
                RoadNodeInput(
                    node_id=str(node_id),
                    label=str(props.get("label", node_id)),
                    node_type=node_type,
                    latitude=latitude,
                    longitude=longitude,
                    external_ref=str(props["external_ref"]) if props.get("external_ref") is not None else None,
                    properties=extra,
                )
            )
            continue

        if geometry_type == "LineString":
            coordinates = _line_coordinates(geometry)
            edge_id = props.get("edge_id")
            source = props.get("source_node_id")
            target = props.get("target_node_id")
            travel = props.get("travel_minutes")
            if not edge_id or not source or not target or travel is None:
                raise NetworkValidationError(
                    "LineString feature requires edge_id, source_node_id, target_node_id and travel_minutes."
                )
            edges.append(
                RoadEdgeInput(
                    edge_id=str(edge_id),
                    source_node_id=str(source),
                    target_node_id=str(target),
                    bidirectional=bool(props.get("bidirectional", True)),
                    travel_minutes=float(travel),
                    distance_meters=float(props["distance_meters"]) if props.get("distance_meters") is not None else None,
                    base_risk=float(props.get("base_risk", 0.0)),
                    current_risk=float(props["current_risk"]) if props.get("current_risk") is not None else None,
                    status=props.get("status", "open"),
                    failure_horizon_minutes=float(props["failure_horizon_minutes"]) if props.get("failure_horizon_minutes") is not None else None,
                    external_ref=str(props["external_ref"]) if props.get("external_ref") is not None else None,
                    geometry_geojson=geometry,
                )
            )
            continue

        raise NetworkValidationError(
            "Only Point node features and LineString road features are accepted."
        )

    return NetworkImportRequest(
        nodes=nodes,
        edges=edges,
        replace_existing=payload.replace_existing,
    )


def import_geojson(
    session: Session,
    payload: GeoJSONFeatureCollection,
    *,
    actor_user_id: int,
):
    return import_network(
        session,
        geojson_to_network(payload),
        actor_user_id=actor_user_id,
    )


def load_bihar_demo_geojson() -> GeoJSONFeatureCollection:
    path = Path(__file__).resolve().parents[2] / "data" / "bihar_supaul_demo.geojson"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return GeoJSONFeatureCollection.model_validate(data)
