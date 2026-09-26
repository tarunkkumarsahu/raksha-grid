from __future__ import annotations

from pydantic import BaseModel, Field

from app.road_network.schemas import RouteResponse


class RoadClosureRequest(BaseModel):
    edge_id: str = Field(min_length=1, max_length=96)
    reason: str = Field(min_length=3, max_length=500)
    origin_node_id: str | None = Field(default=None, min_length=1, max_length=96)
    destination_node_id: str | None = Field(default=None, min_length=1, max_length=96)


class RoadClosureResponse(BaseModel):
    incident_id: int
    edge_id: str
    status: str
    network_version: int
    action: str
    message: str
    rerouted: bool
    route: RouteResponse | None = None
