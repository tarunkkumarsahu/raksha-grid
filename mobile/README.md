# Android App — Kotlin + Jetpack Compose

The Citizen, Responder and Officer screens now read a shared simulation from the FastAPI backend. The Responder can submit a road blockage report; the Officer can approve/reject it; the Citizen's displayed route and modelled isolation timing update after approval.

## Run in Android Studio

1. Start Python backend: `cd backend; python -m uvicorn app.main:app --reload`.
2. Open the `mobile` folder in Android Studio, sync and start an Android emulator.
3. The default API base URL in the app is `http://10.0.2.2:8000` (Android emulator's host loopback).
4. For a physical Android phone on the same Wi-Fi, change the editable Backend URL in the app to your computer's LAN IP (e.g., `http://192.168.x.x:8000`) and run the backend with `--host 0.0.0.0`. Be mindful of firewall settings and only use a trusted local network.
5. For the full incident demonstration, use the Responder screen to report BR-12, then Officer to confirm, then Citizen to see the changed route.

The app uses HTTP cleartext **only for this local prototype**. Production requires HTTPS, real authentication/authorization, field-validated data, persistent storage, offline handling, and audited routing. There is no real GPS/map navigation or verified safe road information yet.
