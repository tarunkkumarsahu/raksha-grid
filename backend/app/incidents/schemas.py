from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


IncidentCategory = Literal["flood", "fire", "blocked_way", "structural", "medical", "other"]
IncidentSeverity = Literal["low", "medium", "high", "critical"]
IncidentStatus = Literal["reported", "active", "resolved", "rejected"]
VerificationStatus = Literal["pending", "verified", "rejected"]
ReporterRole = Literal["citizen", "response_team"]


class IncidentReportCreate(BaseModel):
    category: IncidentCategory
    title: str = Field(min_length=3, max_length=160)
    description: str = Field(min_length=3, max_length=2000)
    severity: IncidentSeverity = "medium"
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    photo_reference: str | None = Field(default=None, max_length=512)
    gps_verified: bool = False
    independent_corroborations: int = Field(default=0, ge=0, le=50)
    contradicting_reports: int = Field(default=0, ge=0, le=50)


class IncidentReviewRequest(BaseModel):
    approve: bool
    note: str | None = Field(default=None, max_length=1000)


class ResolveIncidentRequest(BaseModel):
    note: str | None = Field(default=None, max_length=1000)


class IncidentReportRead(BaseModel):
    id: int
    incident_id: int
    reporter_user_id: int | None
    reporter_role: ReporterRole
    description: str
    latitude: float | None
    longitude: float | None
    photo_reference: str | None
    gps_verified: bool
    independent_corroborations: int
    contradicting_reports: int
    confidence: float
    verification_status: VerificationStatus
    evidence: list[str]
    reviewed_by: str | None
    review_note: str | None
    created_at: datetime
    updated_at: datetime


class AuditEventRead(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    action: str
    actor_type: str
    actor_user_id: int | None
    payload: dict
    created_at: datetime


class IncidentRead(BaseModel):
    id: int
    category: IncidentCategory
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    verification_status: VerificationStatus
    source_type: ReporterRole
    latitude: float | None
    longitude: float | None
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime
    report_count: int = 0


class IncidentDetail(IncidentRead):
    reports: list[IncidentReportRead] = Field(default_factory=list)
    audit_events: list[AuditEventRead] = Field(default_factory=list)
