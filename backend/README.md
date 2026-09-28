# RAKSHA Grid Backend

## Run locally (Windows PowerShell)

~~~powershell
cd backend
py -3.13 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH="."
python -m pytest -q
python -m uvicorn app.main:app --reload
~~~

Open http://127.0.0.1:8000/demo/ui for the **working interactive three-role demo**.
Open http://127.0.0.1:8000/docs for API docs.

## Demo walkthrough

1. Open the Citizen view; note Rampur's suggested route and modelled time to isolation.
2. Switch to Responder and submit a simulated report for BR-12.
3. Switch to Officer; confirm the report. The road graph, citizen route, and isolation estimate update from the shared backend state.
4. Try confirming R-08 too; Rampur then has no modelled route to a shelter.
5. Use Reset to repeat. Browser polls every 2 seconds, so you can use separate tabs for the three roles.

**Safety:** This milestone uses fictional settlements, a schematic network, synthetic failure times, in-memory data, and a demo-only unprotected officer role selector. It is not a real flood forecast or navigation service. Nothing shown is an officially verified safe route.

Next: implement real district GIS datasets, external official-data adapters, actual responder authentication, evidence upload, persistent storage, better UI and formal validation.
