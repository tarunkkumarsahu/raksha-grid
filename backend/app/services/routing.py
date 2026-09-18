import math

import networkx as nx

from app.schemas import SafeCorridorRequest, SafeCorridorResult


RISK_WEIGHT = 2.5


def _edge_cost(travel_minutes: float, hazard_risk: float) -> float:
    return travel_minutes * (1.0 + RISK_WEIGHT * hazard_risk)


def find_safe_corridor(req: SafeCorridorRequest) -> SafeCorridorResult:
    graph = nx.Graph()

    for edge in req.edges:
        if edge.blocked:
            continue
        graph.add_edge(
            edge.source,
            edge.target,
            travel_minutes=edge.travel_minutes,
            hazard_risk=edge.hazard_risk,
            weighted_cost=_edge_cost(edge.travel_minutes, edge.hazard_risk),
        )

    path = nx.shortest_path(graph, req.origin, req.destination, weight="weighted_cost")

    travel = 0.0
    weighted = 0.0
    edge_risks: list[float] = []
    for a, b in zip(path, path[1:]):
        data = graph[a][b]
        travel += data["travel_minutes"]
        weighted += data["weighted_cost"]
        edge_risks.append(data["hazard_risk"])

    route_risk = 0.0 if not edge_risks else 1.0 - math.prod(1.0 - r for r in edge_risks)

    return SafeCorridorResult(
        path=path,
        travel_minutes=round(travel, 1),
        route_risk=round(route_risk, 3),
        weighted_cost=round(weighted, 2),
    )
