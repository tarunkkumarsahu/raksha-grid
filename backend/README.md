# RAKSHA Grid Backend

Private core backend for RAKSHA Grid.

## Local setup

```powershell
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The development database defaults to:

```text
sqlite:///./raksha_grid_dev.db
```

Override it with `DATABASE_URL` when required. PostgreSQL-compatible URLs are supported by SQLAlchemy; production schema changes should be applied through Alembic.

## Database migrations

```powershell
alembic -c alembic.ini upgrade head
```

Create a future revision with:

```powershell
alembic -c alembic.ini revision --autogenerate -m "describe change"
```

## Run

```powershell
$env:PYTHONPATH="."
python -m uvicorn app.main:app --reload --port 8001
```

Open `http://127.0.0.1:8001/docs`.

## Test

```powershell
$env:PYTHONPATH="."
python -m pytest -q
```

## Current persistence milestone

Road closures, shelter capacity, report status, review status, and scenario version are persisted in SQL. Restarting the application no longer intentionally resets those mutable facts. `POST /demo/round1/reset` remains the explicit way to reset the synthetic demo scenario.

The current scenario is still synthetic. Its place names, route graph, hazard values, and time-to-isolation inputs are not official data or certified evacuation guidance.

Current private-core milestones: incident-to-road closure/rerouting, capacity-aware shelter allocation, GeoJSON GIS ingestion, durable notifications/events, and production hardening.

## Authentication (private-core milestone)

The private API now uses two application roles:

- `citizen`
- `response_team`

Register and log in through `/v1/auth/register` and `/v1/auth/login`. Send the returned access token as:

```text
Authorization: Bearer <access_token>
```

Refresh tokens are opaque, stored only as SHA-256 hashes, rotated on refresh, and revocable on logout. Passwords are hashed with Argon2.

Verified Response Team privileges require a configured `RESPONSE_TEAM_REGISTRATION_CODE` during the current private-development stage. This is an onboarding bridge, not the final organization verification workflow.

The `/v1/incidents/*` lifecycle now derives the reporter role from the authenticated account. Clients cannot promote themselves to Response Team by changing request JSON. Review and resolve actions require a verified Response Team account.

The older `/demo/*` endpoints remain intentionally unauthenticated synthetic-demo endpoints and must not be treated as production APIs.


## M5–M9 operational build

The private core now connects the response loop end-to-end:

1. Incident intake and evidence verification.
2. Verified incident -> road-edge closure.
3. Network version bump and immediate rerouting.
4. Shelter allocation using current capacity plus route cost.
5. Response Team capacity updates persisted in the network node state.
6. GeoJSON Point/LineString ingestion plus a synthetic Supaul-style Bihar demo dataset.
7. Role-aware durable notifications and cursor-based event polling.
8. Production configuration checks, trusted hosts, HTTPS redirect, CORS, request IDs, security headers, readiness checks, and a frozen v1.1.0 API contract.

For production deployment, set APP_ENV=production and explicitly configure JWT_SECRET, CORS_ORIGINS, ALLOWED_HOSTS, DATABASE_URL, and the Response Team onboarding mechanism. Run Alembic migrations before starting the API.
