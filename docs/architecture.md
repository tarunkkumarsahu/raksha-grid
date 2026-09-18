# RAKSHA Grid — Milestone 1 Architecture

~~~text
Kotlin Android App
  ├─ Citizen mode
  ├─ Responder mode
  └─ Officer quick view
          │ REST (WebSocket next)
          ▼
Python / FastAPI
  ├─ Isolation Intelligence
  ├─ Safe Corridor Routing
  ├─ Trust-Weighted Ground Intelligence
  └─ Shelter Allocation
          │
          ▼
PostgreSQL + PostGIS (Milestone 2)
          │
          ▼
Official / replay / model / simulation adapters
~~~

## Design rule: provenance before polish

Every datum shown to a user must carry one of these provenance modes:

- live
- official_replay
- model_derived
- simulation

The UI must never make historical or synthetic data look live.

## Milestone sequence

1. **Foundation** — working API contracts, transparent baseline engines, Android shell.
2. **GIS** — selected Bihar district, OSM road graph, settlements, shelters, flood layers.
3. **Dynamic response** — road invalidation, route recomputation, Time-to-Isolation updates.
4. **Realtime** — responder reports propagate to command/citizen views.
5. **Validation** — compare against shortest-route / nearest-shelter baselines.
