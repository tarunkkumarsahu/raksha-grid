# Round 1 working prototype demo (SIMULATION)

Start the backend; open http://127.0.0.1:8000/demo/ui in three browser tabs.

1. Citizen tab: modelled TTI 37 minutes and provisional route to Shelter A.
2. Responder tab: submit `BR-12 / Bridge submerged`; the report is pending review and has **not** blocked the bridge yet.
3. Officer tab: confirm the road closure. The backend removes BR-12 from the graph, updates Rampur TTI to 21 minutes, and recommends Shelter B. No fake alert percentage is claimed.
4. Citizen and responder tabs refresh automatically and show the updated plan.
5. Officer optionally confirms the second road R-08; Rampur now has no route. The UI must show **No modelled evacuation route** rather than send the user into an unsafe road.
6. Reset.

These are **fictional places, hypothetical failure times and a schematic graph**, not Bihar GIS, real flood data, a genuine ML model or verified safe navigation. The 'officer' tab has no authentication and must not be deployed publicly without it.

Actual AI/ML and district GIS remain future milestones. The current isolation estimates use deterministic graph failure simulation, not a trained forecast.
