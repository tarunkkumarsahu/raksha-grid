from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import UserRecord

from .schemas import EventPage, MarkReadRequest, NotificationPage, NotificationRead
from .service import (
    list_events,
    list_notifications,
    mark_all_notifications_read,
    mark_notification_read,
)


router = APIRouter(prefix="/v1", tags=["events"])


@router.get("/notifications", response_model=NotificationPage)
def notifications(
    after_id: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    unread_only: bool = False,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(get_current_user),
) -> NotificationPage:
    return list_notifications(
        db,
        user,
        after_id=after_id,
        limit=limit,
        unread_only=unread_only,
    )


@router.patch("/notifications/{notification_id}", response_model=NotificationRead)
def notification_read(
    notification_id: int,
    payload: MarkReadRequest,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(get_current_user),
) -> NotificationRead:
    try:
        return mark_notification_read(db, user, notification_id, payload.read)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/notifications/read-all")
def notification_read_all(
    db: Session = Depends(get_db),
    user: UserRecord = Depends(get_current_user),
) -> dict[str, int]:
    return {"updated": mark_all_notifications_read(db, user)}


@router.get("/events", response_model=EventPage)
def events(
    after_id: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    user: UserRecord = Depends(get_current_user),
) -> EventPage:
    return list_events(db, user, after_id=after_id, limit=limit)
