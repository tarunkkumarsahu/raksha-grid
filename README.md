# RAKSHA Grid

**From disaster warning to coordinated action.**

RAKSHA Grid is an adaptive disaster-response prototype for the HackMatrix MISC04 problem statement. The intended product connects citizens, field responders and district officers, with a long-term focus on detecting isolation risk, finding viable evacuation corridors, and coordinating shelter decisions.

## Run the Round 1 prototype

This repo currently contains a **working end-to-end, fictional simulation**: a responder files a road closure report, an officer reviews it, and the shared backend recomputes a citizen's modelled route and time to isolation.

~~~powershell
git pull origin main
cd backend
# Activate your existing .venv, if you already created it
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
~~~

Open **http://127.0.0.1:8000/demo/ui** in a browser. Open it in 3 tabs to show Citizen, Responder, and Officer views updating from the same backend state.

For Android, open the `mobile` folder in Android Studio; run an emulator with the backend already started. The app defaults to `http://10.0.2.2:8000` and polls the same demo API. See [mobile/README.md](mobile/README.md).

For the full step-by-step showcase, see [docs/demo-script.md](docs/demo-script.md). For interactive API documentation, open http://127.0.0.1:8000/docs.

## Current vs planned

**Implemented:** FastAPI engines; simulated road graph; report submission and officer review (demo role selector); recomputed routes and modelled isolation timing; browser three-role demo; Android API-connected role views; backend tests and Android build CI.

**Not implemented:** real Bihar GIS ingestion, official live data adapters, validated flood forecasting or trained ML, genuine safety-certified routes, emergency-service integrations, responder authentication, offline navigation and secure production deployment.

**Data integrity:** All example villages, road links, flood exposure, failure times, capacities and travel times are **fictional**. The prototype is **not a live flood monitor or emergency-navigation tool**. Never follow its routes in an actual disaster.

## Technology

- Android: Kotlin + Jetpack Compose
- Backend: Python + FastAPI
- Graph algorithms: NetworkX
- Planned district GIS and persistence: PostgreSQL + PostGIS
- Planned ML: separately trained and evaluated flood-risk prediction

## Team collaboration

Each registered member should contribute meaningful code, design, documentation or tests through their own GitHub account. Never commit secrets, compiled builds, ZIP archives or demonstration videos to the repository.
