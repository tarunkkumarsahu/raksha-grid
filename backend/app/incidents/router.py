from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_response_team
from app.database import get_db
from app.models import UserRecord

from .schemas import (
    IncidentDetail,
    IncidentRead,
    IncidentReportCreate,
    IncidentReviewRequest,
    ResolveIncidentRequest,
)
from .service import (
    IncidentNotFoundError,
    IncidentTransitionError,
    get_incident_detail,
    list_incidents,
    resolve_incident,
    review_incident_report,
    submit_incident_report,
)


router = APIRouter(prefix="/v1/incidents", tags=["incidents"])


def _translate_error(exc: ValueError) -> HTTPException:
    if isinstance(exc, IncidentNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.post("/reports", response_model=IncidentDetail, status_code=status.HTTP_201_CREATED)
def create_incident_report(
    payload: IncidentReportCreate,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(get_current_user),
) -> IncidentDetail:
    return submit_incident_report(
        db,
        payload,
        reporter_role=user.role,
        reporter_user_id=user.id,
        reporter_is_verified=user.is_verified,
    )


@router.post("/reports/{report_id}/review", response_model=IncidentDetail)
def review_report(
    report_id: int,
    payload: IncidentReviewRequest,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> IncidentDetail:
    try:
        return review_incident_report(
            db,
            report_id,
            payload.approve,
            payload.note,
            reviewer_user_id=user.id,
            reviewer_label=user.email,
        )
    except (IncidentNotFoundError, IncidentTransitionError) as exc:
        raise _translate_error(exc) from exc


@router.get("", response_model=list[IncidentRead])
def get_incidents(
    incident_status: Literal["reported", "active", "resolved", "rejected"] | None = Query(
        default=None, alias="status"
    ),
    verification_status: Literal["pending", "verified", "rejected"] | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(get_current_user),
) -> list[IncidentRead]:
    return list_incidents(
        db,
        status=incident_status,
        verification_status=verification_status,
        limit=limit,
    )


@router.get("/{incident_id}", response_model=IncidentDetail)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(get_current_user),
) -> IncidentDetail:
    try:
        return get_incident_detail(db, incident_id)
    except IncidentNotFoundError as exc:
        raise _translate_error(exc) from exc


@router.post("/{incident_id}/resolve", response_model=IncidentDetail)
def resolve(
    incident_id: int,
    payload: ResolveIncidentRequest,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> IncidentDetail:
    try:
        return resolve_incident(
            db,
            incident_id,
            payload.note,
            actor_user_id=user.id,
        )
    except (IncidentNotFoundError, IncidentTransitionError) as exc:
        raise _translate_error(exc) from exc
