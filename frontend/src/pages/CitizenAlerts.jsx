import { Link } from 'react-router-dom';

function CitizenAlerts() {
  return (
    <><div className="flex flex-col w-full relative">
{/*  Ambient Atmospheric Depth Blobs  */}
<div className="absolute -top-10 -left-12 w-64 h-64 bg-primary-fixed-dim/30 rounded-full blur-3xl pointer-events-none -z-10"></div>
<div className="absolute top-72 -right-16 w-72 h-72 bg-secondary-fixed/35 rounded-full blur-3xl pointer-events-none -z-10"></div>
<div className="absolute bottom-20 left-4 w-60 h-60 bg-tertiary-fixed/30 rounded-full blur-3xl pointer-events-none -z-10"></div>
{/*  Navigation Action & Context Row  */}
<div className="flex items-center justify-between gap-space-sm mb-space-md">
<a className="flex items-center gap-space-xs py-2 px-3 rounded-full bg-surface-container-low text-on-surface hover:text-primary transition-all clay-card active:scale-95 group" data-path="home-citizen-dashboard" href="#">
<span className="material-symbols-outlined text-[18px] group-hover:-translate-x-0.5 transition-transform">arrow_back</span>
<span className="font-label-md text-label-md font-bold">Dashboard</span>
</a>
{/*  Tactile Mesh & Sync Pill  */}
<div className="flex items-center gap-1.5 py-1 px-3 rounded-full bg-surface-container clay-card select-none">
<span className="relative flex h-2.5 w-2.5">
<span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"></span>
<span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-secondary"></span>
</span>
<span className="font-label-sm text-label-sm font-bold text-on-surface-variant">Live Sync Active</span>
</div>
</div>
{/*  Friendly Hero Banner  */}
<div className="relative overflow-hidden rounded-lg bg-surface-container-low p-space-lg clay-card mb-space-lg">
<div className="flex items-start justify-between gap-space-md">
<div className="flex flex-col max-w-[75%]">
<span className="font-label-sm text-label-sm uppercase tracking-wider text-primary font-bold mb-1">Incident Broadcasts</span>
<h2 className="font-headline-lg text-headline-lg text-on-surface font-extrabold tracking-tight mb-1">Safety Alerts</h2>
<p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">Important real-time regional updates and life-safety guidance for your radius.</p>
</div>
<div className="w-14 h-14 shrink-0 rounded-2xl bg-primary-container text-on-primary-container flex items-center justify-center clay-pop">
<span className="material-symbols-outlined text-[30px]" >security_update_warning</span>
</div>
</div>
</div>
{/*  Filter Pills Bar (Recessed Track with Clay Filter Buttons)  */}
<div className="mb-space-lg overflow-x-auto no-scrollbar py-1">
<div className="flex items-center gap-space-xs min-w-max p-1 rounded-full bg-surface-container-highest/60" >
<button className="filter-chip active flex items-center gap-1.5 px-4 py-2 rounded-full font-label-md text-label-md transition-all font-bold bg-primary-container text-on-primary-container clay-pop" data-filter="all" type="button">
<span className="material-symbols-outlined text-[16px]">all_inclusive</span>
<span>All Alerts (3)</span>
</button>
<button className="filter-chip flex items-center gap-1.5 px-3.5 py-2 rounded-full font-label-md text-label-md transition-all font-bold bg-surface-container-low text-on-surface-variant hover:text-on-surface clay-card" data-filter="emergency" type="button">
<span className="w-2 h-2 rounded-full bg-secondary-container"></span>
<span>Emergency (1)</span>
</button>
<button className="filter-chip flex items-center gap-1.5 px-3.5 py-2 rounded-full font-label-md text-label-md transition-all font-bold bg-surface-container-low text-on-surface-variant hover:text-on-surface clay-card" data-filter="caution" type="button">
<span className="w-2 h-2 rounded-full bg-secondary-fixed-dim"></span>
<span>Caution (1)</span>
</button>
<button className="filter-chip flex items-center gap-1.5 px-3.5 py-2 rounded-full font-label-md text-label-md transition-all font-bold bg-surface-container-low text-on-surface-variant hover:text-on-surface clay-card" data-filter="info" type="button">
<span className="w-2 h-2 rounded-full bg-tertiary-container"></span>
<span>Info (1)</span>
</button>
</div>
</div>
{/*  Alert Cards Stack  */}
<div className="flex flex-col gap-space-md" id="alertsList">
{/*  Card 1: EMERGENCY  */}
<article className="alert-card group relative flex flex-col rounded-lg bg-surface-container-lowest p-space-md clay-card transition-all duration-200 overflow-hidden" data-category="emergency">
{/*  Hot Pink Accent Depth Stripe  */}
<div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-secondary to-secondary-container"></div>
{/*  Top Badges & Status  */}
<div className="flex items-center justify-between gap-space-xs mb-3 pt-1">
<div className="flex items-center gap-2">
<span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-label-sm text-label-sm uppercase tracking-wider font-extrabold bg-secondary-fixed text-on-secondary-fixed shadow-sm">
<span className="relative flex h-2 w-2">
<span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"></span>
<span className="relative inline-flex rounded-full h-2 w-2 bg-secondary"></span>
</span>
            Emergency • Level 1
          </span>
<span className="text-secondary font-label-sm text-label-sm font-bold flex items-center gap-0.5">
<span className="material-symbols-outlined text-[14px]">warning</span> Action Required
          </span>
</div>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">12 mins ago</span>
</div>
{/*  Icon & Headline Block  */}
<div className="flex items-start gap-space-sm mb-3">
<div className="w-12 h-12 shrink-0 rounded-2xl bg-secondary-container text-on-secondary-container flex items-center justify-center clay-pop">
<span className="material-symbols-outlined text-[24px]">crisis_alert</span>
</div>
<div className="flex flex-col min-w-0">
<h3 className="font-headline-sm text-headline-sm text-on-surface font-extrabold leading-tight tracking-tight">Flash Flood Warning: Riverfront &amp; 4th Ave</h3>
<span className="font-label-sm text-label-sm text-secondary font-semibold mt-0.5 flex items-center gap-1">
<span className="material-symbols-outlined text-[15px]">near_me</span>
            Downtown Sector 4 • 1.2 km away
          </span>
</div>
</div>
{/*  Description & Guidance recessed groove  */}
<div className="p-3 rounded-2xl bg-surface-container-low mb-space-sm text-on-surface-variant font-body-md text-body-md leading-relaxed" >
        Rapidly rising water levels along low-lying river embankments. Evacuate low-lying commercial and residential structures immediately. Do not drive through flooded underpasses.
      </div>
{/*  Location Mini Visual & Actions Footer  */}
<div className="flex items-center justify-between pt-1 gap-2">
<div className="flex items-center gap-1.5 text-on-surface-variant font-label-sm text-label-sm">
<span className="material-symbols-outlined text-[16px] text-secondary">share_location</span>
<span>Safe Route: Elevated Overpass A</span>
</div>
<a className="inline-flex items-center gap-1 px-4 py-2 rounded-full bg-secondary-container text-on-secondary-container font-label-md text-label-md font-bold clay-pop active:scale-95 transition-all" data-path="live-hazard-map" href="#">
<span>View Details</span>
<span className="material-symbols-outlined text-[16px]">arrow_forward</span>
</a>
</div>
</article>
{/*  Card 2: CAUTION  */}
<article className="alert-card group relative flex flex-col rounded-lg bg-surface-container-lowest p-space-md clay-card transition-all duration-200 overflow-hidden" data-category="caution">
{/*  Amber Accent Line  */}
<div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600"></div>
{/*  Top Badges & Status  */}
<div className="flex items-center justify-between gap-space-xs mb-3 pt-1">
<div className="flex items-center gap-2">
<span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-label-sm text-label-sm uppercase tracking-wider font-extrabold bg-amber-100 text-amber-900 shadow-sm">
<span className="inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
            Caution • Advisory
          </span>
<span className="text-amber-800 font-label-sm text-label-sm font-bold flex items-center gap-0.5">
<span className="material-symbols-outlined text-[14px]">traffic</span> Hazard Area
          </span>
</div>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">34 mins ago</span>
</div>
{/*  Icon & Headline Block  */}
<div className="flex items-start gap-space-sm mb-3">
<div className="w-12 h-12 shrink-0 rounded-2xl bg-amber-500 text-on-primary flex items-center justify-center clay-pop">
<span className="material-symbols-outlined text-[24px]">minor_crash</span>
</div>
<div className="flex flex-col min-w-0">
<h3 className="font-headline-sm text-headline-sm text-on-surface font-extrabold leading-tight tracking-tight">Fallen Tree &amp; Power Line on Pine St</h3>
<span className="font-label-sm text-label-sm text-amber-800 font-semibold mt-0.5 flex items-center gap-1">
<span className="material-symbols-outlined text-[15px]">near_me</span>
            North Precinct • 2.5 km away
          </span>
</div>
</div>
{/*  Description recessed box  */}
<div className="p-3 rounded-2xl bg-surface-container-low mb-space-sm text-on-surface-variant font-body-md text-body-md leading-relaxed" >
        Road closed between 7th and 9th Avenue due to downed live electrical lines and obstructed lane. Utility crews and fire services en route. Plan alternate commute.
      </div>
{/*  Footer Info & Button  */}
<div className="flex items-center justify-between pt-1 gap-2">
<div className="flex items-center gap-1.5 text-on-surface-variant font-label-sm text-label-sm">
<span className="material-symbols-outlined text-[16px] text-amber-600">construction</span>
<span>Crews Dispatched</span>
</div>
<a className="inline-flex items-center gap-1 px-4 py-2 rounded-full bg-surface-container text-on-surface font-label-md text-label-md font-bold clay-card hover:bg-surface-container-high active:scale-95 transition-all" data-path="live-hazard-map" href="#">
<span>View Details</span>
<span className="material-symbols-outlined text-[16px]">arrow_forward</span>
</a>
</div>
</article>
{/*  Card 3: INFO  */}
<article className="alert-card group relative flex flex-col rounded-lg bg-surface-container-lowest p-space-md clay-card transition-all duration-200 overflow-hidden" data-category="info">
{/*  Sky Blue Accent Line  */}
<div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-tertiary-fixed-dim via-tertiary-container to-tertiary"></div>
{/*  Top Badges & Status  */}
<div className="flex items-center justify-between gap-space-xs mb-3 pt-1">
<div className="flex items-center gap-2">
<span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-label-sm text-label-sm uppercase tracking-wider font-extrabold bg-tertiary-fixed text-on-tertiary-fixed shadow-sm">
<span className="inline-flex rounded-full h-2 w-2 bg-tertiary"></span>
            Community Notice • Safe Haven
          </span>
<span className="text-tertiary font-label-sm text-label-sm font-bold flex items-center gap-0.5">
<span className="material-symbols-outlined text-[14px]">volunteer_activism</span> Open 24/7
          </span>
</div>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">1 hour ago</span>
</div>
{/*  Icon & Headline Block  */}
<div className="flex items-start gap-space-sm mb-3">
<div className="w-12 h-12 shrink-0 rounded-2xl bg-tertiary-container text-on-tertiary-container flex items-center justify-center clay-pop">
<span className="material-symbols-outlined text-[24px]">night_shelter</span>
</div>
<div className="flex flex-col min-w-0">
<h3 className="font-headline-sm text-headline-sm text-on-surface font-extrabold leading-tight tracking-tight">Emergency Shelter Open: Central High Gym</h3>
<span className="font-label-sm text-label-sm text-tertiary font-semibold mt-0.5 flex items-center gap-1">
<span className="material-symbols-outlined text-[15px]">near_me</span>
            Sector 2 • 3.8 km away
          </span>
</div>
</div>
{/*  Description recessed box  */}
<div className="p-3 rounded-2xl bg-surface-container-low mb-space-sm text-on-surface-variant font-body-md text-body-md leading-relaxed" >
        Clean drinking water, warm nutritional meals, backup power charging, and non-emergency medical triage available. Pets welcome with carriers.
      </div>
{/*  Footer Info & Button  */}
<div className="flex items-center justify-between pt-1 gap-2">
<div className="flex items-center gap-1.5 text-on-surface-variant font-label-sm text-label-sm">
<span className="material-symbols-outlined text-[16px] text-tertiary">pets</span>
<span>Pet Friendly • Wheelchair Access</span>
</div>
<a className="inline-flex items-center gap-1 px-4 py-2 rounded-full bg-surface-container text-on-surface font-label-md text-label-md font-bold clay-card hover:bg-surface-container-high active:scale-95 transition-all" data-path="live-hazard-map" href="#">
<span>View Details</span>
<span className="material-symbols-outlined text-[16px]">arrow_forward</span>
</a>
</div>
</article>
</div>
{/*  Reassuring Verification Footer Card  */}
<div className="mt-space-lg p-space-md rounded-2xl bg-surface-container clay-card flex items-center gap-space-sm">
<div className="w-10 h-10 shrink-0 rounded-full bg-surface-container-lowest flex items-center justify-center text-primary clay-card">
<span className="material-symbols-outlined text-[20px]" >verified_user</span>
</div>
<div className="flex flex-col min-w-0">
<span className="font-title-md text-title-md text-on-surface font-bold">Government Verified Dispatch</span>
<p className="font-body-sm text-body-sm text-on-surface-variant">Alerts broadcast directly from Civil Emergency Operations Center.</p>
</div>
</div>
</div></>
  );
}

export default CitizenAlerts;
