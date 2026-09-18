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

## Build status

Milestone 0 is being bootstrapped: API contracts, first response-intelligence engines, tests, and the Android shell.

> Live, replayed, model-derived, and simulated data will always be labelled separately.
