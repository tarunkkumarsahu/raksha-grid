import { Link } from 'react-router-dom';

function ResponseTeamDashboard() {
  return (
    <><div className="flex flex-col w-full relative px-margin pb-space-xl">
{/*  Ambient Atmospheric Clay Glows  */}
<div className="absolute -top-12 -left-16 w-64 h-64 rounded-full bg-primary/10 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute top-80 -right-16 w-72 h-72 rounded-full bg-secondary-container/10 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute bottom-36 left-1/2 -translate-x-1/2 w-80 h-80 rounded-full bg-tertiary-container/10 blur-3xl pointer-events-none -z-10"></div>
{/*  1. Top Greeting Section  */}
<div className="flex flex-col pt-space-md pb-space-sm">
<div className="flex items-center justify-between">
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-space-xs">
<h1 className="font-headline-md text-headline-md text-on-surface font-extrabold tracking-tight">
            Welcome, Unit Alpha-4
          </h1>
<span className="text-[20px] select-none">🛡️</span>
</div>
<p className="font-body-md text-body-md text-on-surface-variant flex items-center gap-1.5 mt-0.5">
<span className="inline-block w-2 h-2 rounded-full bg-primary-container shadow-[0_0_6px_rgba(124,58,237,0.7)]"></span>
          Sector 4 Downtown Precinct • Active Patrol
        </p>
</div>
{/*  Quick Mesh/Sync Status Bead  */}
<div className="flex items-center gap-1.5 py-1.5 px-3 rounded-full bg-surface-container shadow-[inset_1px_1px_3px_rgba(255,255,255,0.9),3px_4px_10px_rgba(51,47,58,0.06)]">
<span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.7)] animate-ping"></span>
<span className="font-label-sm text-label-sm text-on-surface font-bold">Mesh Live</span>
</div>
</div>
</div>
{/*  2. Current Situation Card (Raised Clay Form)  */}
<section className="mt-space-md rounded-[28px] bg-surface-container-lowest p-space-md shadow-[10px_16px_28px_-4px_rgba(51,47,58,0.08),4px_6px_12px_-2px_rgba(124,58,237,0.05),inset_3px_3px_6px_0px_rgba(255,255,255,0.9),inset_-4px_-4px_8px_0px_rgba(51,47,58,0.04)] relative overflow-hidden">
<div className="flex items-start justify-between gap-space-sm mb-space-sm">
<div className="flex items-center gap-2">
<div className="w-9 h-9 rounded-full bg-surface-container flex items-center justify-center text-primary shadow-[inset_1px_1px_3px_rgba(255,255,255,0.9),2px_3px_8px_rgba(51,47,58,0.07)]">
<span className="material-symbols-outlined text-[20px]">radar</span>
</div>
<h2 className="font-headline-sm text-headline-sm text-on-surface font-bold">
          Current Situation
        </h2>
</div>
{/*  Emerald Monitoring Badge  */}
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
<span className="font-label-sm text-label-sm text-emerald-800 font-bold tracking-tight">Monitoring Active</span>
</div>
</div>
<p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
      Stay alert for new incidents. 3 active dispatches in your tactical response perimeter.
    </p>
{/*  Quick Stats Grid (Pillowy recessed indicators)  */}
<div className="grid grid-cols-3 gap-2 mt-space-md">
<div className="flex flex-col items-center justify-center p-2.5 rounded-2xl bg-surface-container shadow-[inset_2px_2px_5px_rgba(51,47,58,0.07),inset_-2px_-2px_4px_rgba(255,255,255,0.8)]">
<span className="font-headline-sm text-headline-sm text-primary font-black">3</span>
<span className="font-label-sm text-label-sm text-on-surface-variant text-center font-semibold mt-0.5">Active Incidents</span>
</div>
<div className="flex flex-col items-center justify-center p-2.5 rounded-2xl bg-secondary-fixed/50 shadow-[inset_2px_2px_5px_rgba(181,0,93,0.1),inset_-2px_-2px_4px_rgba(255,255,255,0.8)]">
<span className="font-headline-sm text-headline-sm text-secondary font-black">1</span>
<span className="font-label-sm text-label-sm text-on-secondary-fixed-variant text-center font-semibold mt-0.5">High Priority</span>
</div>
<div className="flex flex-col items-center justify-center p-2.5 rounded-2xl bg-surface-container shadow-[inset_2px_2px_5px_rgba(51,47,58,0.07),inset_-2px_-2px_4px_rgba(255,255,255,0.8)]">
<span className="font-headline-sm text-headline-sm text-tertiary font-black">12</span>
<span className="font-label-sm text-label-sm text-on-surface-variant text-center font-semibold mt-0.5">Deployed</span>
</div>
</div>
</section>
{/*  3. Priority Incidents Header  */}
<section className="mt-space-lg flex flex-col gap-space-md">
<div className="flex items-center justify-between">
<div className="flex items-center gap-space-xs">
<h2 className="font-headline-sm text-headline-sm text-on-surface font-extrabold tracking-tight">
          Priority Incidents
        </h2>
<span className="flex items-center justify-center px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-bold shadow-[0_4px_10px_rgba(218,38,118,0.3)]">
          Action Needed (3)
        </span>
</div>
<button className="font-label-sm text-label-sm text-primary font-bold hover:underline">
        Sort: Urgency
      </button>
</div>
{/*  INCIDENT CARD 1: HIGH PRIORITY (Volumetric Clay with crimson accent rim)  */}
<article className="rounded-[28px] bg-surface-container-lowest p-space-md flex flex-col gap-space-sm shadow-[10px_16px_28px_-4px_rgba(51,47,58,0.08),4px_8px_14px_-2px_rgba(218,38,118,0.1),inset_3px_3px_6px_0px_rgba(255,255,255,0.9),inset_-4px_-4px_8px_0px_rgba(51,47,58,0.04)] transition-transform active:scale-[0.99]">
<div className="flex items-center justify-between">
{/*  Urgent Badge  */}
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container shadow-[0_4px_10px_rgba(218,38,118,0.35),inset_1px_1px_2px_rgba(255,255,255,0.4)]">
<span className="material-symbols-outlined text-[16px]">warning</span>
<span className="font-label-sm text-label-sm font-black uppercase tracking-wider">URGENT</span>
</div>
{/*  Status pill: Acknowledged  */}
<div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-500/15 text-amber-900 shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
<span className="font-label-sm text-label-sm font-bold">Acknowledged</span>
</div>
</div>
<div className="flex flex-col mt-0.5">
<h3 className="font-title-md text-title-md text-on-surface font-extrabold leading-snug">
          Flash Flood: Riverfront &amp; 4th Ave
        </h3>
<p className="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1 mt-1">
<span className="material-symbols-outlined text-[16px] text-secondary">distance</span>
          Downtown Sector 4 • 1.2 km away
        </p>
</div>
{/*  Quick Specs pill (recessed groove)  */}
<div className="flex items-center gap-2 p-2.5 rounded-2xl bg-surface-container shadow-[inset_2px_2px_5px_rgba(51,47,58,0.08),inset_-1px_-1px_3px_rgba(255,255,255,0.85)]">
<span className="material-symbols-outlined text-[18px] text-tertiary">water_damage</span>
<span className="font-body-sm text-body-sm text-on-surface font-medium truncate">
          Water level +45cm • Road impassable
        </span>
</div>
<div className="flex items-center justify-between text-on-surface-variant font-body-sm text-body-sm pt-1">
<span className="flex items-center gap-1">
<span className="material-symbols-outlined text-[15px]">schedule</span>
          14 mins ago by Citizen #821
        </span>
</div>
{/*  Tactile Raised Clay Primary Action  */}
<button className="mt-1 w-full h-12 rounded-2xl bg-gradient-to-r from-primary-container to-primary text-on-primary font-label-lg text-label-lg font-bold flex items-center justify-center gap-2 shadow-[0px_10px_20px_-4px_rgba(124,58,237,0.4),inset_2px_2px_4px_0px_rgba(255,255,255,0.45),inset_-3px_-3px_6px_0px_rgba(0,0,0,0.15)] active:scale-95 transition-all" id="btn-incident-1">
<span className="">VIEW INCIDENT</span>
<span className="material-symbols-outlined text-[18px]">arrow_forward</span>
</button>
</article>
{/*  INCIDENT CARD 2: MEDIUM PRIORITY  */}
<article className="rounded-[28px] bg-surface-container-lowest p-space-md flex flex-col gap-space-sm shadow-[10px_16px_28px_-4px_rgba(51,47,58,0.07),inset_3px_3px_6px_0px_rgba(255,255,255,0.9),inset_-4px_-4px_8px_0px_rgba(51,47,58,0.04)] transition-transform active:scale-[0.99]">
<div className="flex items-center justify-between">
{/*  Caution Badge  */}
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/20 text-amber-900 shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="material-symbols-outlined text-[16px] text-amber-700">warning_amber</span>
<span className="font-label-sm text-label-sm font-black uppercase tracking-wider">CAUTION</span>
</div>
{/*  Status pill: In Progress (Sky Blue)  */}
<div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-tertiary-fixed text-on-tertiary-fixed-variant shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
<span className="font-label-sm text-label-sm font-bold">In Progress</span>
</div>
</div>
<div className="flex flex-col mt-0.5">
<h3 className="font-title-md text-title-md text-on-surface font-extrabold leading-snug">
          Fallen Power Line &amp; Debris
        </h3>
<p className="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1 mt-1">
<span className="material-symbols-outlined text-[16px] text-tertiary">near_me</span>
          Pine St &amp; 7th Ave • 2.5 km away
        </p>
</div>
<div className="flex items-center justify-between text-on-surface-variant font-body-sm text-body-sm pt-1">
<span className="flex items-center gap-1">
<span className="material-symbols-outlined text-[15px]">schedule</span>
          32 mins ago by Citizen #744
        </span>
</div>
<button className="mt-1 w-full h-12 rounded-2xl bg-surface-container text-primary font-label-lg text-label-lg font-bold flex items-center justify-center gap-2 shadow-[inset_2px_2px_4px_rgba(255,255,255,0.9),4px_6px_12px_rgba(51,47,58,0.06)] active:scale-95 transition-all" id="btn-incident-2">
<span className="">VIEW INCIDENT</span>
<span className="material-symbols-outlined text-[18px]">arrow_forward</span>
</button>
</article>
{/*  INCIDENT CARD 3: LOW PRIORITY  */}
<article className="rounded-[28px] bg-surface-container-lowest p-space-md flex flex-col gap-space-sm shadow-[10px_16px_28px_-4px_rgba(51,47,58,0.06),inset_3px_3px_6px_0px_rgba(255,255,255,0.9),inset_-4px_-4px_8px_0px_rgba(51,47,58,0.04)] transition-transform active:scale-[0.99]">
<div className="flex items-center justify-between">
{/*  Low Priority Monitoring Badge  */}
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-on-surface-variant shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="material-symbols-outlined text-[16px]">visibility</span>
<span className="font-label-sm text-label-sm font-bold uppercase tracking-wider">MONITORING</span>
</div>
{/*  Status pill: New  */}
<div className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-variant text-on-surface shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="w-1.5 h-1.5 rounded-full bg-primary-container"></span>
<span className="font-label-sm text-label-sm font-bold">New</span>
</div>
</div>
<div className="flex flex-col mt-0.5">
<h3 className="font-title-md text-title-md text-on-surface font-extrabold leading-snug">
          Minor Structural Masonry Crack
        </h3>
<p className="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1 mt-1">
<span className="material-symbols-outlined text-[16px]">location_on</span>
          Westlake Ave • 3.8 km away
        </p>
</div>
<button className="mt-1 w-full h-12 rounded-2xl bg-surface-container text-on-surface font-label-lg text-label-lg font-bold flex items-center justify-center gap-2 shadow-[inset_2px_2px_4px_rgba(255,255,255,0.9),4px_6px_12px_rgba(51,47,58,0.06)] active:scale-95 transition-all" id="btn-incident-3">
<span className="">VIEW INCIDENT</span>
<span className="material-symbols-outlined text-[18px]">arrow_forward</span>
</button>
</article>
</section>
{/*  4. Operational Map Snapshot  */}
<section className="mt-space-lg flex flex-col gap-space-sm">
<div className="flex items-center justify-between">
<div className="flex items-center gap-space-xs">
<span className="material-symbols-outlined text-primary text-[22px]">explore</span>
<h2 className="font-headline-sm text-headline-sm text-on-surface font-extrabold">
          Tactical Incident Map
        </h2>
</div>
<span className="font-label-sm text-label-sm text-on-surface-variant">Live Mesh Overlay</span>
</div>
{/*  Map Container Frame with tactile borderless shadow  */}
<div className="relative w-full rounded-[28px] overflow-hidden bg-surface-container p-2 shadow-[10px_16px_28px_-4px_rgba(51,47,58,0.1),inset_3px_3px_6px_rgba(255,255,255,0.85)]">
{/*  Static Google Maps Static pipeline div  */}
<div className="w-full h-56 rounded-[22px] bg-cover bg-center relative overflow-hidden shadow-[inset_2px_2px_5px_rgba(51,47,58,0.2)]" data-location="Downtown Metropolitan Sector 4" >
{/*  Scrim for contrast  */}
<div className="absolute inset-0 bg-gradient-to-t from-inverse-surface/60 via-transparent to-inverse-surface/20 pointer-events-none"></div>
{/*  Tactical Map Marker Clay Overlays  */}
{/*  Responder Pin (Unit Alpha-4)  */}
<div className="absolute top-1/2 left-1/3 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center">
<div className="w-9 h-9 rounded-full bg-primary-container text-on-primary flex items-center justify-center shadow-[0_6px_14px_rgba(124,58,237,0.5),inset_2px_2px_3px_rgba(255,255,255,0.6)] animate-bounce">
<span className="material-symbols-outlined text-[20px]">local_police</span>
</div>
<span className="mt-1 px-2 py-0.5 rounded-full bg-surface-container-lowest/90 backdrop-blur-sm text-on-surface font-label-sm text-label-sm font-bold shadow-md">You</span>
</div>
{/*  High Priority Beacon Pin  */}
<div className="absolute top-1/4 right-1/4 flex flex-col items-center">
<div className="relative flex items-center justify-center">
<span className="absolute w-8 h-8 rounded-full bg-secondary-container/40 animate-ping"></span>
<div className="w-8 h-8 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center shadow-[0_6px_12px_rgba(218,38,118,0.5),inset_1px_1px_3px_rgba(255,255,255,0.5)]">
<span className="material-symbols-outlined text-[18px]">flood</span>
</div>
</div>
<span className="mt-1 px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-bold shadow-md">Flood</span>
</div>
{/*  Shelter Perimeter Badge overlay  */}
<div className="absolute bottom-3 left-3 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface/90 backdrop-blur-md shadow-md text-on-surface">
<span className="material-symbols-outlined text-[16px] text-tertiary">night_shelter</span>
<span className="font-label-sm text-label-sm font-bold">Shelter Delta (0.8km)</span>
</div>
</div>
</div>
{/*  Open Map Full Action Button  */}
<button className="mt-2 w-full h-14 rounded-2xl bg-gradient-to-r from-primary-container to-primary text-on-primary font-headline-sm text-headline-sm font-extrabold flex items-center justify-center gap-2.5 shadow-[0px_12px_24px_-4px_rgba(124,58,237,0.45),inset_2px_2px_4px_0px_rgba(255,255,255,0.45),inset_-3px_-3px_6px_0px_rgba(0,0,0,0.18)] active:scale-95 transition-all" id="btn-open-map">
<span className="">OPEN FULL OPERATIONAL MAP</span>
<span className="text-[20px]">🗺️</span>
</button>
</section>
{/*  5. Quick Operational Actions Grid  */}
<section className="mt-space-lg flex flex-col gap-space-sm">
<h2 className="font-headline-sm text-headline-sm text-on-surface font-extrabold">
      Quick Actions
    </h2>
<div className="grid grid-cols-3 gap-space-sm">
{/*  Action 1: All Incidents  */}
<button className="flex flex-col items-center text-center p-space-sm rounded-[24px] bg-surface-container-lowest shadow-[8px_12px_20px_-3px_rgba(51,47,58,0.07),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.03)] active:scale-95 transition-all" id="qa-all-incidents">
<div className="w-12 h-12 rounded-2xl bg-surface-container flex items-center justify-center text-primary shadow-[inset_1px_1px_3px_rgba(255,255,255,0.9),2px_4px_8px_rgba(51,47,58,0.07)] mb-2">
<span className="material-symbols-outlined text-[24px]">view_list</span>
</div>
<span className="font-title-md text-title-md text-on-surface font-bold leading-tight">All Incidents</span>
<span className="font-label-sm text-label-sm text-on-surface-variant mt-0.5">(8 Active)</span>
</button>
{/*  Action 2: Broadcast Alert  */}
<button className="flex flex-col items-center text-center p-space-sm rounded-[24px] bg-surface-container-lowest shadow-[8px_12px_20px_-3px_rgba(51,47,58,0.07),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.03)] active:scale-95 transition-all" id="qa-broadcast">
<div className="w-12 h-12 rounded-2xl bg-secondary-fixed/50 flex items-center justify-center text-secondary shadow-[inset_1px_1px_3px_rgba(255,255,255,0.9),2px_4px_8px_rgba(181,0,93,0.1)] mb-2">
<span className="material-symbols-outlined text-[24px]">podcasts</span>
</div>
<span className="font-title-md text-title-md text-on-surface font-bold leading-tight">Broadcast</span>
<span className="font-label-sm text-label-sm text-on-surface-variant mt-0.5">Area Alert</span>
</button>
{/*  Action 3: Unit Comms  */}
<button className="flex flex-col items-center text-center p-space-sm rounded-[24px] bg-surface-container-lowest shadow-[8px_12px_20px_-3px_rgba(51,47,58,0.07),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.03)] active:scale-95 transition-all" id="qa-comms">
<div className="w-12 h-12 rounded-2xl bg-tertiary-fixed/60 flex items-center justify-center text-tertiary shadow-[inset_1px_1px_3px_rgba(255,255,255,0.9),2px_4px_8px_rgba(0,84,121,0.1)] mb-2">
<span className="material-symbols-outlined text-[24px]">forum</span>
</div>
<span className="font-title-md text-title-md text-on-surface font-bold leading-tight">Unit Comms</span>
<span className="font-label-sm text-label-sm text-on-surface-variant mt-0.5">Direct Radio</span>
</button>
</div>
</section>
{/*  Tactile Micro-Interactions Client Script  */}

</div></>
  );
}

export default ResponseTeamDashboard;
