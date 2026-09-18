from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class DataMode(str, Enum):
    LIVE = "live"
    OFFICIAL_REPLAY = "official_replay"
    MODEL_DERIVED = "model_derived"
    SIMULATION = "simulation"


class SettlementInput(BaseModel):
    id: str
    name: str
    population: int = Field(gt=0)
    vulnerable_population: int = Field(ge=0)
    flood_risk: float = Field(ge=0, le=1)
    route_risk: float = Field(ge=0, le=1)
    medical_urgency: float = Field(ge=0, le=1)
    shelter_accessibility: float = Field(ge=0, le=1)
    predicted_exit_failure_minutes: list[float] = Field(default_factory=list)
    data_mode: DataMode = DataMode.SIMULATION


class IsolationResult(BaseModel):
    settlement_id: str
    settlement_name: str
    time_to_isolation_minutes: float | None
    safe_exits_remaining: int
    priority_score: float
    priority_band: Literal["low", "medium", "high", "critical"]
    explanation: list[str]
    data_mode: DataMode


class GroundReportInput(BaseModel):
    reporter_role: Literal["citizen", "responder", "officer"] = "citizen"
    gps_verified: bool = False
    photo_attached: bool = False
    independent_corroborations: int = Field(default=0, ge=0, le=10)
    age_minutes: float = Field(default=0, ge=0)
    contradicting_reports: int = Field(default=0, ge=0, le=10)


class GroundReportResult(BaseModel):
    confidence: float
    state: Literal["unverified", "caution", "actionable"]
    evidence: list[str]


class RouteEdge(BaseModel):
    source: str
    target: str
    travel_minutes: float = Field(gt=0)
    hazard_risk: float = Field(ge=0, le=1)
    blocked: bool = False


class SafeCorridorRequest(BaseModel):
    origin: str
    destination: str
    edges: list[RouteEdge]


class SafeCorridorResult(BaseModel):
    path: list[str]
    travel_minutes: float
    route_risk: float
    weighted_cost: float


class Shelter(BaseModel):
    id: str
    name: str
    capacity_remaining: int = Field(ge=0)


class ShelterCandidate(BaseModel):
    shelter_id: str
    travel_minutes: float = Field(gt=0)
    route_risk: float = Field(ge=0, le=1)


class ShelterDemand(BaseModel):
    settlement_id: str
    people_to_evacuate: int = Field(gt=0)
    priority_score: float = Field(ge=0, le=100)
    candidates: list[ShelterCandidate]


class ShelterAllocationRequest(BaseModel):
    shelters: list[Shelter]
    demands: list[ShelterDemand]


class ShelterAssignment(BaseModel):
    settlement_id: str
    shelter_id: str | None
    people_assigned: int
    unassigned_people: int


class ShelterAllocationResult(BaseModel):
    assignments: list[ShelterAssignment]
    remaining_capacity: dict[str, int]
