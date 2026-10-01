from __future__ import annotations

from pydantic import BaseModel, Field

from app.road_network.schemas import RouteResponse


class ShelterRead(BaseModel):
    node_id: str
    name: str
    capacity_total: int | None = Field(default=None, ge=0)
    capacity_remaining: int | None = Field(default=None, ge=0)
    occupied: int | None = Field(default=None, ge=0)
    availability: str
    latitude: float | None = None
    longitude: float | None = None
    source: str = "network"


class ShelterCapacityUpdate(BaseModel):
    capacity_remaining: int = Field(ge=0, le=1_000_000)
    reason: str = Field(default="Field capacity update", min_length=3, max_length=500)


class ShelterAllocationRequest(BaseModel):
    origin_node_id: str = Field(min_length=1, max_length=96)
    people_count: int = Field(gt=0, le=100_000)


class ShelterCandidate(BaseModel):
    shelter: ShelterRead
    route: RouteResponse | None = None
    eligible: bool
    reason: str


class ShelterAllocationResponse(BaseModel):
    origin_node_id: str
    people_count: int
    selected_shelter: ShelterRead | None = None
    selected_route: RouteResponse | None = None
    candidates: list[ShelterCandidate]
    network_version: int
    message: str
