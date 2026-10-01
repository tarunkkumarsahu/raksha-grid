from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


RoadNodeType = Literal["junction", "settlement", "shelter", "hospital", "bridge", "other"]
RoadEdgeStatus = Literal["open", "restricted", "blocked"]


class RoadNodeInput(BaseModel):
    node_id: str = Field(min_length=1, max_length=96)
    label: str = Field(min_length=1, max_length=160)
    node_type: RoadNodeType = "other"
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    external_ref: str | None = Field(default=None, max_length=160)
    properties: dict = Field(default_factory=dict)


class RoadEdgeInput(BaseModel):
    edge_id: str = Field(min_length=1, max_length=96)
    source_node_id: str = Field(min_length=1, max_length=96)
    target_node_id: str = Field(min_length=1, max_length=96)
    bidirectional: bool = True
    travel_minutes: float = Field(gt=0, le=1440)
    distance_meters: float | None = Field(default=None, ge=0)
    base_risk: float = Field(default=0.0, ge=0, le=1)
    current_risk: float | None = Field(default=None, ge=0, le=1)
    status: RoadEdgeStatus = "open"
    failure_horizon_minutes: float | None = Field(default=None, ge=0)
    external_ref: str | None = Field(default=None, max_length=160)
    geometry_geojson: dict | None = None

    @model_validator(mode="after")
    def different_endpoints(self):
        if self.source_node_id == self.target_node_id:
            raise ValueError("Road edge source and target must be different.")
        return self


class NetworkImportRequest(BaseModel):
    nodes: list[RoadNodeInput] = Field(min_length=1, max_length=5000)
    edges: list[RoadEdgeInput] = Field(default_factory=list, max_length=20000)
    replace_existing: bool = False


class RoadEdgeStatusUpdate(BaseModel):
    status: RoadEdgeStatus
    current_risk: float | None = Field(default=None, ge=0, le=1)
    failure_horizon_minutes: float | None = Field(default=None, ge=0)


class RouteRequest(BaseModel):
    origin_node_id: str = Field(min_length=1, max_length=96)
    destination_node_id: str = Field(min_length=1, max_length=96)

    @model_validator(mode="after")
    def different_nodes(self):
        if self.origin_node_id == self.destination_node_id:
            raise ValueError("Origin and destination must be different.")
        return self


class RoadNodeRead(RoadNodeInput):
    created_at: datetime
    updated_at: datetime


class RoadEdgeRead(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    bidirectional: bool
    travel_minutes: float
    distance_meters: float | None
    base_risk: float
    current_risk: float
    status: RoadEdgeStatus
    failure_horizon_minutes: float | None
    external_ref: str | None
    geometry_geojson: dict | None
    updated_by_user_id: int | None
    created_at: datetime
    updated_at: datetime


class NetworkSnapshot(BaseModel):
    version: int
    nodes: list[RoadNodeRead]
    edges: list[RoadEdgeRead]


class RouteResponse(BaseModel):
    network_version: int
    origin_node_id: str
    destination_node_id: str
    path_nodes: list[str]
    path_edges: list[str]
    travel_minutes: float
    route_risk: float
    weighted_cost: float
    warnings: list[str] = Field(default_factory=list)
