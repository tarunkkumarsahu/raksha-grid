from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_response_team
from app.database import get_db
from app.models import UserRecord
from app.road_network.service import NetworkNotFoundError

from .schemas import CitizenDashboard, ResponseDashboard
from .service import build_citizen_dashboard, build_response_dashboard


router = APIRouter(prefix="/v1/dashboard", tags=["dashboard"])


@router.get("/citizen", response_model=CitizenDashboard)
def citizen_dashboard(
    origin_node_id: str | None = Query(default=None, min_length=1, max_length=96),
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(get_current_user),
) -> CitizenDashboard:
    try:
        return build_citizen_dashboard(db, origin_node_id=origin_node_id)
    except NetworkNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/response", response_model=ResponseDashboard)
def response_dashboard(
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(require_response_team),
) -> ResponseDashboard:
    return build_response_dashboard(db)
