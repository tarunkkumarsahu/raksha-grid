# RAKSHA Grid

**From disaster warning to coordinated action.**

RAKSHA Grid is an adaptive disaster-response and evacuation-intelligence platform. The first implementation focuses on flood response for one Bihar district and is designed around three operational users: **citizen, responder, and district officer**.

## Core intelligence

- **Predictive Isolation Intelligence** — estimates which settlement may lose its last viable access corridor first.
- **Safe Corridor Engine** — chooses the safest viable route rather than the shortest route.
- **Trust-Weighted Ground Intelligence** — fuses citizen and responder reports with confidence and freshness.
- **Capacity-Aware Shelter Allocation** — assigns reachable shelters without overloading capacity.

## Technology direction

- **Android:** Kotlin + Jetpack Compose
- **Backend:** Python + FastAPI
- **GIS / routing / optimization:** Python
- **Database (next milestone):** PostgreSQL + PostGIS
- **Realtime (next milestone):** WebSockets

## Round 1 prototype

The current prototype includes a connected **simulation demo** for Citizen, Responder and Officer roles.

1. Open `GET /demo/round1` to see the pre-disruption state.
2. Submit `POST /demo/round1/report-road` with the default responder evidence for road `B12`.
3. The backend verifies the report confidence.
4. If the report is actionable, Bridge B12 is blocked.
5. RAKSHA Grid recalculates:
   - remaining evacuation exits,
   - Time-to-Isolation,
   - recommended shelter,
   - citizen route,
   - responder approach route,
   - officer priority view.
6. Use `POST /demo/round1/reset` to replay the scenario.

This is deliberately labelled **SIMULATION**. It demonstrates the response workflow without claiming live field deployment.

## Build status

- Baseline isolation, routing, report-confidence and shelter engines: **working**
- Connected dynamic bridge-block scenario: **working**
- Backend tests and CI: **working**
- Android role-based shell: **working UI shell**
- Android ↔ backend integration: **next**
- District GIS / real OSM road network: **next**
- Official-data adapter / replay mode: **next**

> Live, official replay, model-derived, and simulated data will always be labelled separately.
