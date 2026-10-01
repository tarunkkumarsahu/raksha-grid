"""Persistence adapter for the synthetic demo state.

The calculation engines remain stateless. This store persists only mutable
scenario facts (road closures, shelter capacity, reports and state version).
"""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, sessionmaker

from app.database import SessionLocal
from app.models import GroundReportRecord, RoadStatus, ScenarioMeta, ShelterStatus


@dataclass(frozen=True)
class ScenarioState:
    version: int
    blocked_roads: set[str]
    shelter_capacity: dict[str, int]
    reports: list[dict]
    last_report: dict | None


class ScenarioStateStore:
    def __init__(self, session_factory: sessionmaker[Session] = SessionLocal) -> None:
        self._session_factory = session_factory

    @staticmethod
    def _report_to_dict(row: GroundReportRecord) -> dict:
        result = {
            "report_id": row.id,
            "road_id": row.road_id,
            "reason": row.reason,
            "confidence": row.confidence,
            "state": row.state,
            "accepted": row.accepted,
            "status": row.status,
            "evidence": list(row.evidence or []),
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }
        if row.reviewed_by:
            result["reviewed_by"] = row.reviewed_by
        return result

    def ensure_seeded(
        self,
        road_ids: list[str],
        shelter_defaults: dict[str, int],
    ) -> None:
        with self._session_factory.begin() as session:
            meta = session.get(ScenarioMeta, 1)
            if meta is None:
                session.add(ScenarioMeta(id=1, version=0))

            for road_id in road_ids:
                if session.get(RoadStatus, road_id) is None:
                    session.add(RoadStatus(road_id=road_id, blocked=False))

            for shelter_id, capacity in shelter_defaults.items():
                if session.get(ShelterStatus, shelter_id) is None:
                    session.add(
                        ShelterStatus(
                            shelter_id=shelter_id,
                            capacity_remaining=capacity,
                        )
                    )

    def load(self) -> ScenarioState:
        with self._session_factory() as session:
            meta = session.get(ScenarioMeta, 1)
            if meta is None:
                raise RuntimeError("Scenario state has not been initialized.")

            roads = session.scalars(select(RoadStatus).order_by(RoadStatus.road_id)).all()
            shelters = session.scalars(
                select(ShelterStatus).order_by(ShelterStatus.shelter_id)
            ).all()
            report_rows = session.scalars(
                select(GroundReportRecord).order_by(GroundReportRecord.id)
            ).all()

            reports = [self._report_to_dict(row) for row in report_rows]
            return ScenarioState(
                version=meta.version,
                blocked_roads={row.road_id for row in roads if row.blocked},
                shelter_capacity={
                    row.shelter_id: row.capacity_remaining for row in shelters
                },
                reports=reports,
                last_report=reports[-1] if reports else None,
            )

    def reset(
        self,
        road_ids: list[str],
        shelter_defaults: dict[str, int],
    ) -> ScenarioState:
        self.ensure_seeded(road_ids, shelter_defaults)
        with self._session_factory.begin() as session:
            for road_id in road_ids:
                row = session.get(RoadStatus, road_id)
                if row is not None:
                    row.blocked = False

            for shelter_id, capacity in shelter_defaults.items():
                row = session.get(ShelterStatus, shelter_id)
                if row is not None:
                    row.capacity_remaining = capacity

            session.execute(delete(GroundReportRecord))
            meta = session.get(ScenarioMeta, 1)
            assert meta is not None
            meta.version += 1

        return self.load()

    def record_report(self, entry: dict, *, block_road: bool) -> dict:
        with self._session_factory.begin() as session:
            road = session.get(RoadStatus, entry["road_id"])
            if road is None:
                raise ValueError("Unknown demo road ID.")

            row = GroundReportRecord(
                road_id=entry["road_id"],
                reason=entry["reason"],
                confidence=float(entry["confidence"]),
                state=entry["state"],
                accepted=bool(entry["accepted"]),
                status=entry["status"],
                evidence=list(entry.get("evidence", [])),
            )
            session.add(row)
            session.flush()

            if block_road:
                road.blocked = True

            meta = session.get(ScenarioMeta, 1)
            if meta is None:
                raise RuntimeError("Scenario state has not been initialized.")
            meta.version += 1
            session.flush()
            result = self._report_to_dict(row)

        return result

    def review_report(self, report_id: int, approve: bool) -> dict:
        with self._session_factory.begin() as session:
            row = session.get(GroundReportRecord, report_id)
            if row is None:
                raise ValueError("Unknown report ID.")
            if row.status != "pending":
                raise ValueError("Only pending reports can be reviewed.")

            row.status = "accepted" if approve else "rejected"
            row.accepted = approve
            row.reviewed_by = "demo_response_team"

            if approve:
                road = session.get(RoadStatus, row.road_id)
                if road is None:
                    raise ValueError("Unknown demo road ID.")
                road.blocked = True

            meta = session.get(ScenarioMeta, 1)
            if meta is None:
                raise RuntimeError("Scenario state has not been initialized.")
            meta.version += 1
            session.flush()
            result = self._report_to_dict(row)

        return result

    def set_shelter_capacity(self, shelter_id: str, capacity_remaining: int) -> None:
        with self._session_factory.begin() as session:
            row = session.get(ShelterStatus, shelter_id)
            if row is None:
                raise ValueError("Unknown demo shelter ID.")
            row.capacity_remaining = capacity_remaining

            meta = session.get(ScenarioMeta, 1)
            if meta is None:
                raise RuntimeError("Scenario state has not been initialized.")
            meta.version += 1
