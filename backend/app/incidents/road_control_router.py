from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import require_response_team
from app.database import get_db
from app.models import UserRecord

from .road_control_schemas import RoadClosureRequest, RoadClosureResponse
from .road_control_service import IncidentRoadLinkError, close_incident_road, reopen_incident_road


router = APIRouter(prefix="/v1/incidents", tags=["incident-road-controls"])


@router.post(
    "/{incident_id}/road-closure",
    response_model=RoadClosureResponse,
)
def close_road_from_incident(
    incident_id: int,
    payload: RoadClosureRequest,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> RoadClosureResponse:
    try:
        return close_incident_road(
            db,
            incident_id,
            payload,
            actor_user_id=user.id,
        )
    except IncidentRoadLinkError as exc:
        message = str(exc)
        code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=code, detail=message) from exc


@router.post(
    "/{incident_id}/road-reopen",
    response_model=RoadClosureResponse,
)
def reopen_road_from_incident(
    incident_id: int,
    payload: RoadClosureRequest,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> RoadClosureResponse:
    try:
        return reopen_incident_road(
            db,
            incident_id,
            payload,
            actor_user_id=user.id,
        )
    except IncidentRoadLinkError as exc:
        message = str(exc)
        code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=code, detail=message) from exc
