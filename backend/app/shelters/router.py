from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_response_team
from app.database import get_db
from app.models import UserRecord
from app.road_network.service import NetworkNotFoundError

from .schemas import (
    ShelterAllocationRequest,
    ShelterAllocationResponse,
    ShelterCapacityUpdate,
    ShelterRead,
)
from .service import allocate_shelter, list_shelters, update_shelter_capacity


router = APIRouter(prefix="/v1/shelters", tags=["shelters"])


@router.get("", response_model=list[ShelterRead])
def shelters(
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(get_current_user),
) -> list[ShelterRead]:
    return list_shelters(db)


@router.patch("/{node_id}/capacity", response_model=ShelterRead)
def change_shelter_capacity(
    node_id: str,
    payload: ShelterCapacityUpdate,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> ShelterRead:
    try:
        return update_shelter_capacity(
            db,
            node_id,
            payload,
            actor_user_id=user.id,
        )
    except NetworkNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.post("/allocate", response_model=ShelterAllocationResponse)
def allocate(
    payload: ShelterAllocationRequest,
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(get_current_user),
) -> ShelterAllocationResponse:
    try:
        return allocate_shelter(db, payload)
    except NetworkNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
