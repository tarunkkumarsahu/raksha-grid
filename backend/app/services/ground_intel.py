import math

from app.schemas import GroundReportInput, GroundReportResult


ROLE_BASE = {
    "citizen": 0.28,
    "responder": 0.55,
    "officer": 0.68,
}


def score_ground_report(report: GroundReportInput) -> GroundReportResult:
    confidence = ROLE_BASE[report.reporter_role]
    evidence: list[str] = [f"Reporter role: {report.reporter_role}."]

    if report.gps_verified:
        confidence += 0.10
        evidence.append("GPS location verified.")
    if report.photo_attached:
        confidence += 0.10
        evidence.append("Photo evidence attached.")

    confidence += min(0.22, report.independent_corroborations * 0.055)
    if report.independent_corroborations:
        evidence.append(f"{report.independent_corroborations} independent corroboration(s).")

    confidence -= min(0.30, report.contradicting_reports * 0.075)
    if report.contradicting_reports:
        evidence.append(f"{report.contradicting_reports} contradicting report(s).")

    confidence *= math.exp(-report.age_minutes / 180.0)
    if report.age_minutes > 30:
        evidence.append("Confidence reduced because the report is aging.")

    confidence = round(max(0.0, min(0.99, confidence)), 2)
    state = "actionable" if confidence >= 0.75 else "caution" if confidence >= 0.45 else "unverified"

    return GroundReportResult(confidence=confidence, state=state, evidence=evidence)
