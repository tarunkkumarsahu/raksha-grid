# RAKSHA Grid Backend

## Run locally

~~~bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
~~~

Open http://127.0.0.1:8000/docs for the interactive API.

## Test

~~~bash
pytest -q
~~~

The first milestone intentionally uses transparent deterministic baselines. GIS ingestion, PostGIS persistence, OR-Tools optimization, and realtime events are subsequent milestones.
