from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high", "critical"]
RiskBand = Literal["low", "medium", "high", "critical", "unknown"]
DashboardMode = Literal["simulation", "network"]


class DashboardAlert(BaseModel):
    id: str
    title: str
    category: str
    severity: Severity
    status: str
    verification_status: str
    message: str
    latitude: float | None = None
    longitude: float | None = None
    source: str
    created_at: datetime | None = None


class DashboardShelter(BaseModel):
    id: str
    name: str
    capacity_remaining: int | None = Field(default=None, ge=0)
    availability: Literal["available", "limited", "full", "unknown"]
    source: str


class DashboardRoute(BaseModel):
    available: bool
    destination_id: str | None = None
    destination_name: str | None = None
    path_nodes: list[str] = Field(default_factory=list)
    path_edges: list[str] = Field(default_factory=list)
    travel_minutes: float | None = None
    route_risk: float | None = Field(default=None, ge=0, le=1)
    weighted_cost: float | None = None
    warnings: list[str] = Field(default_factory=list)
    source: str


class CitizenDashboard(BaseModel):
    mode: DashboardMode
    notice: str
    location: str
    risk: RiskBand
    time_to_isolation_minutes: float | None
    alerts: list[DashboardAlert]
    shelters: list[DashboardShelter]
    route: DashboardRoute
    version: int


class PriorityIncident(BaseModel):
    id: int
    title: str
    category: str
    severity: Severity
    status: str
    verification_status: str
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime
    report_count: int


class PendingReport(BaseModel):
    id: int
    incident_id: int
    reporter_role: str
    confidence: float
    created_at: datetime


class ResponseDashboard(BaseModel):
    mode: DashboardMode
    notice: str
    active_incidents: int
    high_priority_incidents: int
    pending_reports: int
    blocked_roads: list[str]
    network_version: int
    priority_incidents: list[PriorityIncident]
    pending_report_queue: list[PendingReport]
    version: int
