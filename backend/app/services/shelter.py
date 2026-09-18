from app.schemas import (
    ShelterAllocationRequest,
    ShelterAllocationResult,
    ShelterAssignment,
)


def allocate_shelters(req: ShelterAllocationRequest) -> ShelterAllocationResult:
    """Greedy, explainable baseline allocator.

    Higher-priority settlements are allocated first. Each settlement prefers the
    candidate with the lowest risk-adjusted travel cost that still has capacity.
    This will later be benchmarked against an OR-Tools optimizer.
    """
    remaining = {s.id: s.capacity_remaining for s in req.shelters}
    assignments: list[ShelterAssignment] = []

    for demand in sorted(req.demands, key=lambda d: d.priority_score, reverse=True):
        ranked = sorted(
            demand.candidates,
            key=lambda c: c.travel_minutes * (1 + 2.5 * c.route_risk),
        )

        people_left = demand.people_to_evacuate
        assigned_shelter: str | None = None
        assigned_people = 0

        for candidate in ranked:
            available = remaining.get(candidate.shelter_id, 0)
            if available <= 0:
                continue
            take = min(people_left, available)
            remaining[candidate.shelter_id] -= take
            people_left -= take
            assigned_people += take
            if assigned_shelter is None:
                assigned_shelter = candidate.shelter_id
            if people_left == 0:
                break

        assignments.append(
            ShelterAssignment(
                settlement_id=demand.settlement_id,
                shelter_id=assigned_shelter,
                people_assigned=assigned_people,
                unassigned_people=people_left,
            )
        )

    return ShelterAllocationResult(assignments=assignments, remaining_capacity=remaining)
