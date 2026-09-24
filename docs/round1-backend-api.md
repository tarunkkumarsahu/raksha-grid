# Round 1 backend — mobile and officer API contract

## Running the demo

Run one backend process from the `backend` folder:

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

On the same laptop, browse to http://127.0.0.1:8001/docs .
For an Android emulator, use `http://10.0.2.2:8001` as the API base URL.
For a physical Android phone, use `http://<LAPTOP_WIFI_IPV4>:8001` on the same Wi-Fi; permit the port in Windows Firewall when prompted. The phone cannot reach the laptop via `127.0.0.1`.

The Android project needs `android.permission.INTERNET`; for development-only HTTP, configure network security to allow cleartext to the local server. Do not ship a public Android app with unrestricted HTTP. Use HTTPS and authenticated roles for any real deployment.

## Shared endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/demo/round1` | Snapshot for Citizen, Responder and Officer. Includes `version`, `roads`, `settlements` and `shelters`. |
| POST | `/demo/round1/report-road` | Submit road report; responder evidence can block a valid road in the *simulation*. |
| POST | `/demo/round1/reports/{report_id}/review` | Officer approves or rejects a pending demo report. |
| PATCH | `/demo/round1/shelters/{shelter_id}/capacity` | Set remaining capacity and recalculate all views. |
| POST | `/demo/round1/reset` | Return to demo state; `version` increments. |

Run all role views against the same server. Poll `GET /demo/round1` every 2–3 seconds and update the UI **only when `version` changes**. The citizen should show `citizen.route_status`; if `unavailable`, show `citizen.message`, not a navigation button. Treat route paths as names of *synthetic graph nodes*, not actual turn-by-turn geographic guidance.

Example responder report:

```json
{
  "road_id": "B12",
  "reason": "Bridge flooded",
  "reporter_role": "responder",
  "gps_verified": true,
  "photo_attached": true,
  "independent_corroborations": 2,
  "age_minutes": 2,
  "contradicting_reports": 0
}
```

Report review request body: `{"approve": true}`. Shelter update body: `{"capacity_remaining": 0}`.

All IDs and all locations are **SIMULATION**. This demo has *no authentication*: reporter role, GPS and photo flags are self-declared. These values are not verified by the backend and MUST NOT be described as a real trust or safety assurance. An approved report blocks a demo road, not a real road. Official alerts and on-ground authorities must always take precedence.

## Tests

```powershell
cd backend
$env:PYTHONPATH="."
python -m pytest -q
```

## Known prototype limitations

- This model contains 11 illustrative graph edges and three fictional settlements; no GIS coordinates or real district roads.
- The 37/82-minute exit-failure times are fixed scenario assumptions, not predictions from live flood data or trained ML.
- Shelter capacity is input by a demo operator; selecting a shelter does NOT reserve a space or prevent simultaneous allocation.
- Shared state is stored in memory. Use a single Uvicorn worker. Restarting loses reports/capacity and multiple workers will diverge.
- Citizen and responder views report route nodes as simulated guidance, not certified safe evacuation instructions.
- Member 1 owns Android screen/API integration. This backend contract makes it possible but does not implement the app integration itself.
