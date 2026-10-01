from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.events.service import emit_notification
from app.models import AuditEventRecord, IncidentRecord, IncidentReportRecord, utcnow
from app.schemas import GroundReportInput
from app.services.ground_intel import score_ground_report

from .schemas import IncidentDetail, IncidentRead, IncidentReportCreate


class IncidentNotFoundError(ValueError):
    pass


class IncidentTransitionError(ValueError):
    pass


def _map_role_for_scoring(role: str) -> str:
    return "responder" if role == "response_team" else "citizen"


def _incident_read(session: Session, incident: IncidentRecord) -> IncidentRead:
    report_count = session.scalar(
        select(func.count(IncidentReportRecord.id)).where(
            IncidentReportRecord.incident_id == incident.id
        )
    ) or 0
    return IncidentRead(
        id=incident.id,
        category=incident.category,
        title=incident.title,
        description=incident.description,
        severity=incident.severity,
        status=incident.status,
        verification_status=incident.verification_status,
        source_type=incident.source_type,
        latitude=incident.latitude,
        longitude=incident.longitude,
        resolved_at=incident.resolved_at,
        created_at=incident.created_at,
        updated_at=incident.updated_at,
        report_count=int(report_count),
    )


def get_incident_detail(session: Session, incident_id: int) -> IncidentDetail:
    incident = session.get(IncidentRecord, incident_id)
    if incident is None:
        raise IncidentNotFoundError("Incident not found.")

    reports = session.scalars(
        select(IncidentReportRecord)
        .where(IncidentReportRecord.incident_id == incident_id)
        .order_by(IncidentReportRecord.id)
    ).all()
    events = session.scalars(
        select(AuditEventRecord)
        .where(
            AuditEventRecord.entity_type == "incident",
            AuditEventRecord.entity_id == incident_id,
        )
        .order_by(AuditEventRecord.id)
    ).all()

    base = _incident_read(session, incident)
    return IncidentDetail(
        **base.model_dump(),
        reports=[
            {
                "id": report.id,
                "incident_id": report.incident_id,
                "reporter_user_id": report.reporter_user_id,
                "reporter_role": report.reporter_role,
                "description": report.description,
                "latitude": report.latitude,
                "longitude": report.longitude,
                "photo_reference": report.photo_reference,
                "gps_verified": report.gps_verified,
                "independent_corroborations": report.independent_corroborations,
                "contradicting_reports": report.contradicting_reports,
                "confidence": report.confidence,
                "verification_status": report.verification_status,
                "evidence": list(report.evidence or []),
                "reviewed_by": report.reviewed_by,
                "review_note": report.review_note,
                "created_at": report.created_at,
                "updated_at": report.updated_at,
            }
            for report in reports
        ],
        audit_events=[
            {
                "id": event.id,
                "entity_type": event.entity_type,
                "entity_id": event.entity_id,
                "action": event.action,
                "actor_type": event.actor_type,
                "actor_user_id": event.actor_user_id,
                "payload": dict(event.payload or {}),
                "created_at": event.created_at,
            }
            for event in events
        ],
    )


def submit_incident_report(
    session: Session,
    payload: IncidentReportCreate,
    *,
    reporter_role: str,
    reporter_user_id: int,
    reporter_is_verified: bool,
) -> IncidentDetail:
    score = score_ground_report(
        GroundReportInput(
            reporter_role=_map_role_for_scoring(reporter_role),
            gps_verified=payload.gps_verified,
            photo_attached=payload.photo_reference is not None,
            independent_corroborations=payload.independent_corroborations,
            age_minutes=0,
            contradicting_reports=payload.contradicting_reports,
        )
    )

    auto_verify = (
        reporter_role == "response_team"
        and reporter_is_verified
        and score.state == "actionable"
        and payload.contradicting_reports == 0
    )
    if auto_verify:
        verification_status = "verified"
        incident_status = "active"
    elif score.confidence >= 0.25:
        verification_status = "pending"
        incident_status = "reported"
    else:
        verification_status = "rejected"
        incident_status = "rejected"

    incident = IncidentRecord(
        category=payload.category,
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        status=incident_status,
        verification_status=verification_status,
        source_type=reporter_role,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    session.add(incident)
    session.flush()

    report = IncidentReportRecord(
        incident_id=incident.id,
        reporter_user_id=reporter_user_id,
        reporter_role=reporter_role,
        description=payload.description,
        latitude=payload.latitude,
        longitude=payload.longitude,
        photo_reference=payload.photo_reference,
        gps_verified=payload.gps_verified,
        independent_corroborations=payload.independent_corroborations,
        contradicting_reports=payload.contradicting_reports,
        confidence=score.confidence,
        verification_status=verification_status,
        evidence=list(score.evidence),
    )
    session.add(report)
    session.add(
        AuditEventRecord(
            entity_type="incident",
            entity_id=incident.id,
            action="incident_report_submitted",
            actor_type=reporter_role,
            actor_user_id=reporter_user_id,
            payload={
                "reporter_role": reporter_role,
                "verification_status": verification_status,
                "confidence": score.confidence,
            },
        )
    )

    if verification_status == "verified":
        emit_notification(
            session,
            event_type="incident.verified",
            severity=incident.severity,
            title="Verified hazard reported",
            message=incident.title,
            target_role="citizen",
            entity_type="incident",
            entity_id=incident.id,
            payload={
                "category": incident.category,
                "latitude": incident.latitude,
                "longitude": incident.longitude,
            },
        )
    elif verification_status == "pending":
        emit_notification(
            session,
            event_type="incident.pending",
            severity="medium",
            title="New incident needs verification",
            message=incident.title,
            target_role="response_team",
            entity_type="incident",
            entity_id=incident.id,
        )

    session.commit()
    return get_incident_detail(session, incident.id)


def list_incidents(
    session: Session,
    status: str | None = None,
    verification_status: str | None = None,
    limit: int = 50,
) -> list[IncidentRead]:
    query = select(IncidentRecord).order_by(IncidentRecord.created_at.desc()).limit(limit)
    if status:
        query = query.where(IncidentRecord.status == status)
    if verification_status:
        query = query.where(IncidentRecord.verification_status == verification_status)

    incidents = session.scalars(query).all()
    return [_incident_read(session, incident) for incident in incidents]


def review_incident_report(
    session: Session,
    report_id: int,
    approve: bool,
    note: str | None,
    *,
    reviewer_user_id: int,
    reviewer_label: str,
) -> IncidentDetail:
    report = session.get(IncidentReportRecord, report_id)
    if report is None:
        raise IncidentNotFoundError("Incident report not found.")
    if report.verification_status != "pending":
        raise IncidentTransitionError("Only pending incident reports can be reviewed.")

    incident = session.get(IncidentRecord, report.incident_id)
    if incident is None:
        raise IncidentNotFoundError("Incident not found.")

    report.verification_status = "verified" if approve else "rejected"
    report.reviewed_by = reviewer_label
    report.review_note = note
    incident.verification_status = "verified" if approve else "rejected"
    incident.status = "active" if approve else "rejected"

    session.add(
        AuditEventRecord(
            entity_type="incident",
            entity_id=incident.id,
            action="incident_report_approved" if approve else "incident_report_rejected",
            actor_type="response_team",
            actor_user_id=reviewer_user_id,
            payload={"report_id": report.id, "note": note},
        )
    )

    if approve:
        if report.reporter_user_id is not None:
            emit_notification(
                session,
                event_type="incident.verified",
                severity=incident.severity,
                title="Your incident report was verified",
                message=incident.title,
                user_id=report.reporter_user_id,
                entity_type="incident",
                entity_id=incident.id,
            )
        emit_notification(
            session,
            event_type="incident.verified",
            severity=incident.severity,
            title="Verified hazard is now active",
            message=incident.title,
            target_role="citizen",
            entity_type="incident",
            entity_id=incident.id,
        )
    elif report.reporter_user_id is not None:
        emit_notification(
            session,
            event_type="incident.rejected",
            severity="medium",
            title="Incident report rejected",
            message=incident.title,
            user_id=report.reporter_user_id,
            entity_type="incident",
            entity_id=incident.id,
        )

    session.commit()
    return get_incident_detail(session, incident.id)


def resolve_incident(
    session: Session,
    incident_id: int,
    note: str | None,
    *,
    actor_user_id: int,
) -> IncidentDetail:
    incident = session.get(IncidentRecord, incident_id)
    if incident is None:
        raise IncidentNotFoundError("Incident not found.")
    if incident.status != "active":
        raise IncidentTransitionError("Only active incidents can be resolved.")

    incident.status = "resolved"
    incident.resolved_at = utcnow()
    session.add(
        AuditEventRecord(
            entity_type="incident",
            entity_id=incident.id,
            action="incident_resolved",
            actor_type="response_team",
            actor_user_id=actor_user_id,
            payload={"note": note},
        )
    )
    emit_notification(
        session,
        event_type="incident.resolved",
        severity="low",
        title="Incident resolved",
        message=incident.title,
        target_role="citizen",
        entity_type="incident",
        entity_id=incident.id,
    )
    session.commit()
    return get_incident_detail(session, incident.id)
