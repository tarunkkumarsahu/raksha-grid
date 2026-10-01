# RAKSHA Grid frontend API contract

This document is the integration contract for the Kotlin/Jetpack Compose app. The UI must not hard-code operational state such as Seattle labels, fake incident counts, or shelter availability.

## Authentication

1. POST /v1/auth/register
2. POST /v1/auth/login
3. Store the access token in the Android secure token mechanism selected by the frontend team.
4. Send Authorization: Bearer <access_token> for protected calls.
5. Use POST /v1/auth/refresh when the access token expires.

## Citizen screens

### Home / alerts

GET /v1/dashboard/citizen

Optional query parameter: origin_node_id when the GIS network is loaded. Without it, the endpoint returns the labelled synthetic Bihar-style demo state.

The response supplies:
- location and risk
- time_to_isolation_minutes
- alerts[]
- shelters[]
- route
- mode and notice

### Incident report

POST /v1/incidents/reports

The app sends category, title, description, GPS coordinates, photo reference, GPS verification and corroboration fields. The API returns the created incident plus its verification state.

### Incident details

GET /v1/incidents/{incident_id}

Use this for a report/alert detail screen.

## Response Team screens

### Dashboard

GET /v1/dashboard/response

Provides active incident count, high-priority count, pending report count, blocked roads, network version, priority incidents and pending report queue.

### Incident review

POST /v1/incidents/reports/{report_id}/review

Response Team only. Approve or reject a pending report.

### Road controls

- GET /v1/network
- PATCH /v1/network/edges/{edge_id}
- POST /v1/network/import
- POST /v1/network/route

Response Team can import/update the network. Both roles can request a route.

## Demo rule

If mode is simulation, show a visible SIMULATION badge in the UI. Never label synthetic locations or predicted times as live government/GIS data.


## Shelters

- GET /v1/shelters
- POST /v1/shelters/allocate with origin_node_id and people_count
- PATCH /v1/shelters/{node_id}/capacity is Response Team only.

Allocation considers both remaining capacity and current network route cost.

## Incident → road → reroute

After a verified incident exists, Response Team can call:

POST /v1/incidents/{incident_id}/road-closure

The request may include edge_id, reason, origin_node_id and destination_node_id. The API blocks the edge, increments network_version and can return the recalculated route in the same response.

Road reopening uses POST /v1/incidents/{incident_id}/road-reopen.

## Notifications and events

- GET /v1/notifications?after_id=...&limit=...
- PATCH /v1/notifications/{notification_id}
- POST /v1/notifications/read-all
- GET /v1/events?after_id=...&limit=...

Use after_id as a durable cursor for polling. Notifications are role-aware and persisted in SQL.

## GIS import

Response Team can import a GeoJSON FeatureCollection through POST /v1/network/import/geojson.

The private core also exposes POST /v1/network/import/demo-bihar, which loads the repository's synthetic Supaul-style Bihar demo network. The dataset is explicitly simulation-only.
