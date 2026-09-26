from __future__ import annotations

from datetime import datetime
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import AuditEventRecord, NotificationRecord, UserRecord, utcnow

from .schemas import EventPage, EventRead, NotificationPage, NotificationRead


def emit_notification(
    session: Session,
    *,
    event_type: str,
    severity: str,
    title: str,
    message: str,
    target_role: str | None = None,
    user_id: int | None = None,
    entity_type: str | None = None,
    entity_id: int | None = None,
    payload: dict | None = None,
) -> NotificationRecord:
    if target_role is None and user_id is None:
        raise ValueError("Notification requires a target role or user.")
    notification = NotificationRecord(
        user_id=user_id,
        target_role=target_role,
        event_type=event_type,
        severity=severity,
        title=title,
        message=message,
        entity_type=entity_type,
        entity_id=entity_id,
        payload=dict(payload or {}),
        created_at=utcnow(),
    )
    session.add(notification)
    session.flush()
    return notification


def _notification_read(row: NotificationRecord) -> NotificationRead:
    return NotificationRead(
        id=row.id,
        event_type=row.event_type,
        severity=row.severity,
        title=row.title,
        message=row.message,
        entity_type=row.entity_type,
        entity_id=row.entity_id,
        payload=dict(row.payload or {}),
        read_at=row.read_at,
        created_at=row.created_at,
    )


def _visible_filter(user: UserRecord):
    return or_(
        NotificationRecord.user_id == user.id,
        NotificationRecord.user_id.is_(None)
        & (NotificationRecord.target_role == user.role),
    )


def list_notifications(
    session: Session,
    user: UserRecord,
    *,
    after_id: int = 0,
    limit: int = 50,
    unread_only: bool = False,
) -> NotificationPage:
    query = (
        select(NotificationRecord)
        .where(_visible_filter(user), NotificationRecord.id > after_id)
        .order_by(NotificationRecord.id.asc())
        .limit(limit)
    )
    if unread_only:
        query = query.where(NotificationRecord.read_at.is_(None))
    rows = session.scalars(query).all()
    unread = session.scalar(
        select(NotificationRecord.id)
        .where(_visible_filter(user), NotificationRecord.read_at.is_(None))
        .order_by(NotificationRecord.id.desc())
        .limit(1)
    )
    unread_count = 0
    if unread is not None:
        unread_count = session.query(NotificationRecord).filter(
            _visible_filter(user), NotificationRecord.read_at.is_(None)
        ).count()
    return NotificationPage(
        items=[_notification_read(row) for row in rows],
        unread_count=unread_count,
        next_after_id=rows[-1].id if rows else None,
    )


def mark_notification_read(
    session: Session,
    user: UserRecord,
    notification_id: int,
    read: bool,
) -> NotificationRead:
    row = session.scalar(
        select(NotificationRecord).where(
            NotificationRecord.id == notification_id,
            _visible_filter(user),
        )
    )
    if row is None:
        raise ValueError("Notification not found.")
    row.read_at = utcnow() if read else None
    session.commit()
    return _notification_read(row)


def mark_all_notifications_read(session: Session, user: UserRecord) -> int:
    rows = session.scalars(
        select(NotificationRecord).where(
            _visible_filter(user),
            NotificationRecord.read_at.is_(None),
        )
    ).all()
    now = utcnow()
    for row in rows:
        row.read_at = now
    session.commit()
    return len(rows)


def list_events(
    session: Session,
    user: UserRecord,
    *,
    after_id: int = 0,
    limit: int = 100,
) -> EventPage:
    query = (
        select(AuditEventRecord)
        .where(AuditEventRecord.id > after_id)
        .order_by(AuditEventRecord.id.asc())
        .limit(limit)
    )
    if user.role == "citizen":
        query = query.where(
            AuditEventRecord.action.in_(
                {
                    "incident_report_approved",
                    "incident_resolved",
                    "road_closed_from_incident",
                    "road_reopened_from_incident",
                    "shelter_capacity_updated",
                }
            )
        )
    rows = session.scalars(query).all()
    return EventPage(
        items=[
            EventRead(
                id=row.id,
                entity_type=row.entity_type,
                entity_id=row.entity_id,
                action=row.action,
                actor_type=row.actor_type,
                actor_user_id=row.actor_user_id,
                payload=dict(row.payload or {}),
                created_at=row.created_at,
            )
            for row in rows
        ],
        next_after_id=rows[-1].id if rows else None,
    )
