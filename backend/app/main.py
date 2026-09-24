from typing import Literal

import networkx as nx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.schemas import (
    GroundReportInput,
    GroundReportResult,
    IsolationResult,
    SafeCorridorRequest,
    SafeCorridorResult,
    SettlementInput,
    ShelterAllocationRequest,
    ShelterAllocationResult,
)
from app.services.demo_scenario import demo_scenario
from app.services.ground_intel import score_ground_report
from app.services.isolation import compute_isolation_intelligence
from app.services.routing import find_safe_corridor
from app.services.shelter import allocate_shelters


class DemoRoadReport(BaseModel):
    road_id: str = Field(default="B12", min_length=2, max_length=30)
    reason: str = Field(default="Bridge flooded / blocked", min_length=3, max_length=240)
    reporter_role: Literal["citizen", "responder", "officer"] = "responder"
    gps_verified: bool = True
    photo_attached: bool = True
    independent_corroborations: int = Field(default=2, ge=0, le=10)
    age_minutes: float = Field(default=2, ge=0)
    contradicting_reports: int = Field(default=0, ge=0, le=10)


app = FastAPI(
    title="RAKSHA Grid API",
    version="0.3.0",
    description="Response-intelligence API for adaptive flood evacuation and coordination.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "raksha-grid-api", "version": "0.3.0"}


@app.post("/intelligence/isolation", response_model=IsolationResult)
def isolation_intelligence(payload: SettlementInput) -> IsolationResult:
    return compute_isolation_intelligence(payload)


@app.post("/intelligence/ground-report", response_model=GroundReportResult)
def ground_report(payload: GroundReportInput) -> GroundReportResult:
    return score_ground_report(payload)


@app.post("/routing/safe-corridor", response_model=SafeCorridorResult)
def safe_corridor(payload: SafeCorridorRequest) -> SafeCorridorResult:
    try:
        return find_safe_corridor(payload)
    except (nx.NetworkXNoPath, nx.NodeNotFound) as exc:
        raise HTTPException(status_code=422, detail="No viable route exists for this scenario.") from exc


@app.post("/shelters/allocate", response_model=ShelterAllocationResult)
def shelters(payload: ShelterAllocationRequest) -> ShelterAllocationResult:
    return allocate_shelters(payload)


@app.get("/demo/situation")
def demo_situation() -> dict:
    """Small labelled simulation used to wire the first mobile demo."""
    settlements = [
        SettlementInput(
            id="VIL-B",
            name="Rampur",
            population=1840,
            vulnerable_population=510,
            flood_risk=0.88,
            route_risk=0.73,
            medical_urgency=0.35,
            shelter_accessibility=0.55,
            predicted_exit_failure_minutes=[37],
            data_mode="simulation",
        ),
        SettlementInput(
            id="VIL-A",
            name="Basantpur",
            population=4200,
            vulnerable_population=760,
            flood_risk=0.79,
            route_risk=0.46,
            medical_urgency=0.20,
            shelter_accessibility=0.80,
            predicted_exit_failure_minutes=[38, 74, 105],
            data_mode="simulation",
        ),
    ]
    ranked = sorted(
        [compute_isolation_intelligence(s) for s in settlements],
        key=lambda x: x.priority_score,
        reverse=True,
    )
    return {
        "mode": "simulation",
        "notice": "Synthetic demo scenario. Do not present this endpoint as live official data.",
        "priority_settlements": [r.model_dump() for r in ranked],
    }


@app.get("/demo/round1")
def round1_demo() -> dict:
    """Get the current connected Citizen / Responder / Officer demo state."""
    return demo_scenario.snapshot()


@app.post("/demo/round1/reset")
def reset_round1_demo() -> dict:
    """Reset the demo to the pre-disruption state."""
    return demo_scenario.reset()


@app.post("/demo/round1/report-road")
def report_road(payload: DemoRoadReport) -> dict:
    """Submit a field report and update the road only if evidence is actionable."""
    report = GroundReportInput(
        reporter_role=payload.reporter_role,
        gps_verified=payload.gps_verified,
        photo_attached=payload.photo_attached,
        independent_corroborations=payload.independent_corroborations,
        age_minutes=payload.age_minutes,
        contradicting_reports=payload.contradicting_reports,
    )
    try:
        return demo_scenario.report_blocked_road(
            road_id=payload.road_id,
            report=report,
            reason=payload.reason,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


class DemoReportReview(BaseModel):
    approve: bool


class DemoShelterCapacity(BaseModel):
    capacity_remaining: int = Field(ge=0, le=100000)


@app.post("/demo/round1/reports/{report_id}/review")
def review_road_report(report_id: int, payload: DemoReportReview) -> dict:
    """Officer review action for a PENDING report. Simulation only; no user auth."""
    try:
        return demo_scenario.review_report(report_id, payload.approve)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.patch("/demo/round1/shelters/{shelter_id}/capacity")
def update_shelter_capacity(shelter_id: str, payload: DemoShelterCapacity) -> dict:
    """Set the remaining demo shelter capacity and recalculate all role views."""
    try:
        return demo_scenario.set_capacity(shelter_id, payload.capacity_remaining)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
