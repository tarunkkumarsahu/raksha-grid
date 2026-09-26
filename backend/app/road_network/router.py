from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_response_team
from app.database import get_db
from app.models import UserRecord

from .gis import import_geojson, load_bihar_demo_geojson
from .gis_schemas import GeoJSONFeatureCollection
from .schemas import (
    NetworkImportRequest,
    NetworkSnapshot,
    RoadEdgeRead,
    RoadEdgeStatusUpdate,
    RouteRequest,
    RouteResponse,
)
from .service import (
    NetworkNotFoundError,
    NetworkValidationError,
    NoRouteError,
    find_route,
    get_network_snapshot,
    import_network,
    update_edge_status,
)


router = APIRouter(prefix="/v1/network", tags=["road-network"])


@router.get("", response_model=NetworkSnapshot)
def network_snapshot(
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(get_current_user),
) -> NetworkSnapshot:
    return get_network_snapshot(db)


@router.post("/import", response_model=NetworkSnapshot)
def load_network(
    payload: NetworkImportRequest,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> NetworkSnapshot:
    try:
        return import_network(db, payload, actor_user_id=user.id)
    except NetworkValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.patch("/edges/{edge_id}", response_model=RoadEdgeRead)
def change_edge_status(
    edge_id: str,
    payload: RoadEdgeStatusUpdate,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> RoadEdgeRead:
    try:
        return update_edge_status(
            db,
            edge_id,
            payload,
            actor_user_id=user.id,
        )
    except NetworkNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/route", response_model=RouteResponse)
def route(
    payload: RouteRequest,
    db: Session = Depends(get_db),
    _user: UserRecord = Depends(get_current_user),
) -> RouteResponse:
    try:
        return find_route(db, payload)
    except NetworkNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except NoRouteError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post("/import/geojson", response_model=NetworkSnapshot)
def load_geojson_network(
    payload: GeoJSONFeatureCollection,
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> NetworkSnapshot:
    try:
        return import_geojson(db, payload, actor_user_id=user.id)
    except NetworkValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post("/import/demo-bihar", response_model=NetworkSnapshot)
def load_bihar_demo_network(
    db: Session = Depends(get_db),
    user: UserRecord = Depends(require_response_team),
) -> NetworkSnapshot:
    try:
        payload = load_bihar_demo_geojson()
        return import_geojson(db, payload, actor_user_id=user.id)
    except (NetworkValidationError, OSError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Bihar demo dataset could not be loaded: {exc}",
        ) from exc
