from app.schemas import IsolationResult, SettlementInput


def _priority_band(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 35:
        return "medium"
    return "low"


def compute_isolation_intelligence(item: SettlementInput) -> IsolationResult:
    """Transparent baseline for settlement isolation urgency.

    Time-to-Isolation (TTI) is the predicted failure time of the last currently
    viable exit. If no usable exit remains, TTI is 0. This is intentionally a
    deterministic baseline, not a trained ML model.
    """
    usable_exit_failures = [m for m in item.predicted_exit_failure_minutes if m > 0]
    safe_exits = len(usable_exit_failures)
    tti = max(usable_exit_failures) if usable_exit_failures else 0.0

    vulnerability_ratio = min(1.0, item.vulnerable_population / max(1, item.population))
    isolation_urgency = 1.0 if tti == 0 else max(0.0, min(1.0, (90.0 - tti) / 90.0))
    exit_fragility = 1.0 if safe_exits <= 1 else max(0.0, 1.0 - ((safe_exits - 1) * 0.2))

    score = 100 * (
        0.30 * isolation_urgency
        + 0.18 * exit_fragility
        + 0.18 * item.flood_risk
        + 0.12 * item.route_risk
        + 0.10 * vulnerability_ratio
        + 0.07 * item.medical_urgency
        + 0.05 * (1.0 - item.shelter_accessibility)
    )
    score = round(max(0.0, min(100.0, score)), 1)

    explanation: list[str] = []
    if safe_exits == 0:
        explanation.append("No viable evacuation exit remains.")
    elif safe_exits == 1:
        explanation.append("Only one viable evacuation exit remains.")
    else:
        explanation.append(f"{safe_exits} viable evacuation exits remain.")

    if tti > 0:
        explanation.append(f"Last viable exit is estimated to fail in about {tti:.0f} minutes.")
    if item.flood_risk >= 0.7:
        explanation.append("Flood exposure is high.")
    if vulnerability_ratio >= 0.25:
        explanation.append("A large share of the population is vulnerable.")
    if item.shelter_accessibility <= 0.4:
        explanation.append("Shelter accessibility is limited.")

    return IsolationResult(
        settlement_id=item.id,
        settlement_name=item.name,
        time_to_isolation_minutes=round(tti, 1),
        safe_exits_remaining=safe_exits,
        priority_score=score,
        priority_band=_priority_band(score),
        explanation=explanation,
        data_mode=item.data_mode,
    )
