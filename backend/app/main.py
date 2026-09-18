import networkx as nx
from fastapi import FastAPI, HTTPException

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
from app.services.ground_intel import score_ground_report
from app.services.isolation import compute_isolation_intelligence
from app.services.routing import find_safe_corridor
from app.services.shelter import allocate_shelters

app = FastAPI(
    title="RAKSHA Grid API",
    version="0.1.0",
    description="Response-intelligence API for adaptive flood evacuation and coordination.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "raksha-grid-api", "version": "0.1.0"}


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
