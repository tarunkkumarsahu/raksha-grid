# RAKSHA Grid API Contract Freeze — v1.1.0

Status: **frozen for the reviewed private-core snapshot**

This document defines the API surface that the Android/Kotlin frontend can integrate against without depending on implementation details.

## 1. Stable API rules

- /v1/* is the supported application API namespace.
- JSON request/response shapes are the integration contract.
- Unknown response fields may be added without breaking clients; existing fields are not renamed or removed in a compatible release.
- Network version changes whenever a road closure/reopen, network import, or shelter-capacity update changes routing state.
- mode=simulation means synthetic demo data and must be visibly labelled in the UI.
- Production clients must not treat synthetic route, risk, capacity, or time values as official emergency guidance.

## 2. Authentication

- POST /v1/auth/register
- POST /v1/auth/login
- POST /v1/auth/refresh
- POST /v1/auth/logout
- GET /v1/auth/me

Roles are exactly:
- citizen
- response_team

Response Team operational actions require a verified account.

## 3. Citizen / shared APIs

- GET /v1/dashboard/citizen
- POST /v1/incidents/reports
- GET /v1/incidents
- GET /v1/incidents/{incident_id}
- POST /v1/network/route
- GET /v1/network
- GET /v1/shelters
- POST /v1/shelters/allocate
- GET /v1/notifications
- PATCH /v1/notifications/{notification_id}
- POST /v1/notifications/read-all
- GET /v1/events

## 4. Response Team APIs

- GET /v1/dashboard/response
- POST /v1/incidents/reports/{report_id}/review
- POST /v1/incidents/{incident_id}/resolve
- POST /v1/incidents/{incident_id}/road-closure
- POST /v1/incidents/{incident_id}/road-reopen
- PATCH /v1/network/edges/{edge_id}
- POST /v1/network/import
- POST /v1/network/import/geojson
- POST /v1/network/import/demo-bihar
- PATCH /v1/shelters/{node_id}/capacity

## 5. Operational pipeline

1. A citizen or verified Response Team submits an incident.
2. Ground evidence produces a confidence/verification state.
3. Response Team verifies pending incidents.
4. A verified incident can be linked to a road edge and close it.
5. Network version increments and blocked edges are removed from routing.
6. The same closure call can return an alternate route when origin/destination are supplied.
7. Shelter allocation filters by current capacity and current route cost.
8. State changes emit durable notifications and audit events.
9. Android clients poll notifications/events using after_id cursors.

## 6. GIS contract

GeoJSON import accepts a FeatureCollection containing:
- Point features for nodes
- LineString features for road edges

Point properties require node_id; road properties require edge_id, source_node_id, target_node_id, and travel_minutes.

backend/data/bihar_supaul_demo.geojson is a synthetic demo dataset. Its geometry, shelter capacities and route values are not an official government GIS dataset.

## 7. Health / deployment

- GET /health is a liveness endpoint.
- GET /health/ready checks database readiness.
- Production requires explicit JWT_SECRET, CORS_ORIGINS, and ALLOWED_HOSTS.
- Production disables interactive OpenAPI/Swagger/ReDoc endpoints.
- Production adds HTTPS redirect, trusted-host validation, request IDs and baseline security headers.

## 8. Compatibility policy

Any breaking API change requires a new /v2 namespace or a separately reviewed contract revision. Do not silently change the semantics of existing /v1 fields.
