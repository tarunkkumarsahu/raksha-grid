import { Link } from 'react-router-dom';

function ResponseTeamIncidents() {
  return (
    <><div className="flex flex-col w-full relative">
{/*  Ambient Atmospheric Glowing Backdrops  */}
<div className="absolute -top-12 -left-20 w-72 h-72 rounded-full bg-primary-fixed-dim/30 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute top-96 -right-24 w-80 h-80 rounded-full bg-secondary-fixed/40 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute bottom-40 left-10 w-64 h-64 rounded-full bg-tertiary-fixed/30 blur-3xl pointer-events-none -z-10"></div>
{/*  Top Action & Navigation Context  */}
<div className="px-margin pt-space-md pb-space-sm flex items-center justify-between">
<div className="flex items-center gap-space-sm">
<a className="w-11 h-11 rounded-full bg-surface-container flex items-center justify-center text-on-surface shadow-[4px_6px_12px_rgba(51,47,58,0.08),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.06)] active:scale-95 transition-all" data-path="dashboard" href="#" aria-label="Back to Response Team Dashboard">
<span className="material-symbols-outlined text-[22px]">arrow_back</span>
</a>
<div>
<h1 className="font-headline-sm text-headline-sm text-on-surface tracking-tight leading-none">Operational Incidents</h1>
<p className="font-label-sm text-label-sm text-on-surface-variant mt-0.5">Real-time field response feed</p>
</div>
</div>
{/*  Tactile Quick Signal Pill  */}
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container shadow-[2px_3px_8px_rgba(51,47,58,0.06),inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="w-2 h-2 rounded-full bg-secondary animate-ping"></span>
<span className="font-label-sm text-label-sm text-secondary font-bold tracking-wide">MESH ON</span>
</div>
</div>
{/*  Search & Filter Controls  */}
<section className="px-margin py-space-sm flex flex-col gap-space-sm">
{/*  Recessed Clay Search Box  */}
<div className="w-full relative flex items-center">
<span className="material-symbols-outlined absolute left-4 text-on-surface-variant/70 text-[20px] pointer-events-none">search</span>
<input className="w-full pl-11 pr-4 py-3 rounded-full bg-surface-container-high text-on-surface font-body-md text-body-md placeholder:text-outline shadow-[inset_3px_3px_6px_rgba(51,47,58,0.1),inset_-2px_-2px_4px_rgba(255,255,255,0.85)] focus:outline-none focus:shadow-[inset_2px_2px_4px_rgba(51,47,58,0.12),0_0_0_3px_rgba(124,58,237,0.25)] transition-all" id="incident-search" placeholder="Search by sector, type, or ID..." type="text" />
</div>
{/*  Filter Pills Horizontal Strip (Tactile Clay)  */}
<div className="flex items-center gap-space-xs overflow-x-auto no-scrollbar py-1">
<button className="filter-pill flex-shrink-0 px-4 py-2 rounded-full font-label-md text-label-md font-bold bg-primary-container text-on-primary shadow-[0_8px_16px_rgba(124,58,237,0.32),inset_2px_2px_3px_rgba(255,255,255,0.45),inset_-2px_-2px_4px_rgba(0,0,0,0.2)] active:scale-95 transition-all" data-filter="all">
        All (8)
      </button>
<button className="filter-pill flex-shrink-0 px-4 py-2 rounded-full font-label-md text-label-md font-medium bg-surface-container text-on-surface shadow-[3px_5px_10px_rgba(51,47,58,0.06),inset_2px_2px_3px_rgba(255,255,255,0.8),inset_-2px_-2px_3px_rgba(51,47,58,0.04)] active:scale-95 transition-all" data-filter="active">
        Active (5)
      </button>
<button className="filter-pill flex-shrink-0 px-4 py-2 rounded-full font-label-md text-label-md font-medium bg-surface-container text-on-surface shadow-[3px_5px_10px_rgba(51,47,58,0.06),inset_2px_2px_3px_rgba(255,255,255,0.8),inset_-2px_-2px_3px_rgba(51,47,58,0.04)] active:scale-95 transition-all" data-filter="high">
        High Priority (2)
      </button>
<button className="filter-pill flex-shrink-0 px-4 py-2 rounded-full font-label-md text-label-md font-medium bg-surface-container text-on-surface shadow-[3px_5px_10px_rgba(51,47,58,0.06),inset_2px_2px_3px_rgba(255,255,255,0.8),inset_-2px_-2px_3px_rgba(51,47,58,0.04)] active:scale-95 transition-all" data-filter="resolved">
        Resolved (3)
      </button>
</div>
</section>
{/*  Incident Card Feed  */}
<section className="px-margin flex flex-col gap-space-md mt-space-xs" id="incident-feed">
{/*  Card 1: Flash Flood  */}
<article className="incident-card rounded-lg p-space-md bg-surface-container-lowest shadow-[8px_14px_22px_-4px_rgba(51,47,58,0.08),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-3px_-3px_6px_rgba(51,47,58,0.03)] flex flex-col gap-space-sm relative overflow-hidden transition-all duration-200" data-priority="high" data-status="active" data-path="incident-details">
<div className="flex items-start justify-between gap-space-xs">
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-error-container text-on-error-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8),inset_-1px_-1px_2px_rgba(186,26,26,0.15)]">
<span className="material-symbols-outlined text-[16px] text-error">flood</span>
<span className="font-label-sm text-label-sm uppercase font-bold tracking-wider text-error">HIGH PRIORITY</span>
</div>
<div className="px-3 py-1 rounded-full bg-secondary-fixed text-on-secondary-fixed font-label-sm text-label-sm font-semibold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.7)]">
          Acknowledged
        </div>
</div>
<div className="flex flex-col gap-0.5">
<h2 className="font-headline-sm text-headline-sm text-on-surface font-bold tracking-tight">Flash Flood: Riverfront &amp; 4th Ave</h2>
<div className="flex items-center gap-1 text-on-surface-variant font-body-sm text-body-sm">
<span className="material-symbols-outlined text-[16px] text-primary">near_me</span>
<span className="">Sector 4 • 1.2 km away</span>
</div>
</div>
{/*  Tactical Visual Snapshot Placeholders  */}
<div className="flex items-center gap-space-xs py-0.5">
<div className="w-14 h-14 rounded-DEFAULT overflow-hidden shadow-[inset_1px_1px_2px_rgba(255,255,255,0.6)]">
<img className="w-full h-full object-cover"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCK-vIaQ7Q8qE34m4uc81FHp3ukYOBfY2UdDCi-XyMZDqJNnuH7OLv4Zxef6pDkZ-HbJRzM0TWtUj1YMAEvYT8ihP1Q_CKcFEIpB4r1dLOT_ZquH8mHcoiofpP4iqQ3sbSx0wVe5sM1n1ZbqTa-_Vgkd529xpG1qN9SZftlO0UkZyWEyL-8AaoA56kXw4pM_EfmbRXF566QUmGVGEztHDf1_U7fT1v_3KXxaLcLK1Y4q3-O0c2rsaEdDQ" />
</div>
<div className="w-14 h-14 rounded-DEFAULT overflow-hidden shadow-[inset_1px_1px_2px_rgba(255,255,255,0.6)]">
<img className="w-full h-full object-cover"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuDx6l6Ap4gFa9AiK4Ye0sKIHEKuXckkuu4BQ88FrHc0WUGCmOWfXZXcDf7gWp_0XPn6FIBp3i69V5qipLPkRAhCrQKGSxOtfsGmi6L4hevSFx7wNTFNQcDi60rd0iqeugCRoyPIQ18pasDCYpdcXI6pEfnK3RAoH6qWOTrhMRsmZqZ8rEWREPWqigncy9j1X9pv-H0oi9WohCzuggj77sM6WTrP0DeG2Aot5jj_Si_26qvGlXVplOKnyQ" />
</div>
<div className="flex-1 h-14 rounded-DEFAULT bg-surface-container flex flex-col justify-center px-3 shadow-[inset_2px_2px_4px_rgba(51,47,58,0.06),inset_-1px_-1px_2px_rgba(255,255,255,0.9)]">
<span className="font-label-sm text-label-sm text-on-surface font-bold">14 mins ago</span>
<span className="font-body-sm text-body-sm text-on-surface-variant truncate">Citizen Verified (3 photos)</span>
</div>
</div>
{/*  Action Button: Popped Clay Primary  */}
<button className="w-full py-3.5 rounded-DEFAULT bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center gap-2 shadow-[0_12px_20px_rgba(124,58,237,0.32),inset_2px_2px_3px_rgba(255,255,255,0.45),inset_-3px_-3px_5px_rgba(0,0,0,0.18)] active:scale-[0.98] transition-all">
<span className="">VIEW INCIDENT</span>
<span className="material-symbols-outlined text-[20px]">arrow_forward</span>
</button>
</article>
{/*  Card 2: Gas Odor  */}
<article className="incident-card rounded-lg p-space-md bg-surface-container-lowest shadow-[8px_14px_22px_-4px_rgba(51,47,58,0.08),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-3px_-3px_6px_rgba(51,47,58,0.03)] flex flex-col gap-space-sm relative overflow-hidden transition-all duration-200" data-priority="high" data-status="active" data-path="incident-details">
<div className="flex items-start justify-between gap-space-xs">
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-error-container text-on-error-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8),inset_-1px_-1px_2px_rgba(186,26,26,0.15)]">
<span className="material-symbols-outlined text-[16px] text-error">mode_heat</span>
<span className="font-label-sm text-label-sm uppercase font-bold tracking-wider text-error">HIGH PRIORITY</span>
</div>
<div className="px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed font-label-sm text-label-sm font-semibold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
          New
        </div>
</div>
<div className="flex flex-col gap-0.5">
<h2 className="font-headline-sm text-headline-sm text-on-surface font-bold tracking-tight">Gas Odor &amp; Transformer Spark</h2>
<div className="flex items-center gap-1 text-on-surface-variant font-body-sm text-body-sm">
<span className="material-symbols-outlined text-[16px] text-primary">location_on</span>
<span className="">Industrial Park Way • 4.1 km away</span>
</div>
</div>
<div className="p-space-sm rounded-DEFAULT bg-surface-container flex items-center justify-between shadow-[inset_2px_2px_4px_rgba(51,47,58,0.06),inset_-1px_-1px_2px_rgba(255,255,255,0.9)]">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-secondary text-[20px]">sensors</span>
<span className="font-body-md text-body-md text-on-surface font-medium">Automated Sensor Trigger</span>
</div>
<span className="font-label-sm text-label-sm text-on-surface-variant">22 mins ago</span>
</div>
{/*  Action Button  */}
<button className="w-full py-3.5 rounded-DEFAULT bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center gap-2 shadow-[0_12px_20px_rgba(124,58,237,0.32),inset_2px_2px_3px_rgba(255,255,255,0.45),inset_-3px_-3px_5px_rgba(0,0,0,0.18)] active:scale-[0.98] transition-all">
<span className="">VIEW INCIDENT</span>
<span className="material-symbols-outlined text-[20px]">arrow_forward</span>
</button>
</article>
{/*  Card 3: Downed Tree  */}
<article className="incident-card rounded-lg p-space-md bg-surface-container-lowest shadow-[8px_14px_22px_-4px_rgba(51,47,58,0.08),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-3px_-3px_6px_rgba(51,47,58,0.03)] flex flex-col gap-space-sm relative overflow-hidden transition-all duration-200" data-priority="medium" data-status="active" data-path="incident-details">
<div className="flex items-start justify-between gap-space-xs">
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-fixed text-on-secondary-fixed shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="material-symbols-outlined text-[16px] text-secondary">power_off</span>
<span className="font-label-sm text-label-sm uppercase font-bold tracking-wider text-secondary">MEDIUM PRIORITY</span>
</div>
<div className="px-3 py-1 rounded-full bg-tertiary-fixed text-on-tertiary-fixed font-label-sm text-label-sm font-semibold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
          In Progress
        </div>
</div>
<div className="flex flex-col gap-0.5">
<h2 className="font-headline-sm text-headline-sm text-on-surface font-bold tracking-tight">Downed Tree &amp; Live Power Line</h2>
<div className="flex items-center gap-1 text-on-surface-variant font-body-sm text-body-sm">
<span className="material-symbols-outlined text-[16px] text-primary">navigation</span>
<span className="">Pine St &amp; 7th Ave • 2.5 km away</span>
</div>
</div>
<div className="p-space-sm rounded-DEFAULT bg-surface-container flex items-center justify-between shadow-[inset_2px_2px_4px_rgba(51,47,58,0.06),inset_-1px_-1px_2px_rgba(255,255,255,0.9)]">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-primary text-[20px]">person_alert</span>
<span className="font-body-md text-body-md text-on-surface font-medium">Citizen Emergency Call</span>
</div>
<span className="font-label-sm text-label-sm text-on-surface-variant">32 mins ago</span>
</div>
{/*  Action Button  */}
<button className="w-full py-3.5 rounded-DEFAULT bg-primary-container text-on-primary font-headline-sm text-headline-sm flex items-center justify-center gap-2 shadow-[0_12px_20px_rgba(124,58,237,0.32),inset_2px_2px_3px_rgba(255,255,255,0.45),inset_-3px_-3px_5px_rgba(0,0,0,0.18)] active:scale-[0.98] transition-all">
<span className="">VIEW INCIDENT</span>
<span className="material-symbols-outlined text-[20px]">arrow_forward</span>
</button>
</article>
{/*  Card 4: Non-Hazard Debris  */}
<article className="incident-card rounded-lg p-space-md bg-surface-container-lowest shadow-[8px_14px_22px_-4px_rgba(51,47,58,0.08),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-3px_-3px_6px_rgba(51,47,58,0.03)] flex flex-col gap-space-sm relative overflow-hidden transition-all duration-200" data-priority="low" data-status="resolved" data-path="incident-details">
<div className="flex items-start justify-between gap-space-xs">
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-high text-on-surface shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<span className="material-symbols-outlined text-[16px] text-tertiary">domain</span>
<span className="font-label-sm text-label-sm uppercase font-bold tracking-wider text-tertiary">LOW PRIORITY</span>
</div>
<div className="px-3 py-1 rounded-full bg-primary-fixed-dim text-on-primary-fixed font-label-sm text-label-sm font-semibold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
          Resolved
        </div>
</div>
<div className="flex flex-col gap-0.5">
<h2 className="font-headline-sm text-headline-sm text-on-surface font-bold tracking-tight">Non-Hazard Debris in Alley</h2>
<div className="flex items-center gap-1 text-on-surface-variant font-body-sm text-body-sm">
<span className="material-symbols-outlined text-[16px] text-primary">place</span>
<span className="">Mercer St • 5.0 km away</span>
</div>
</div>
<div className="p-space-sm rounded-DEFAULT bg-surface-container flex items-center justify-between shadow-[inset_2px_2px_4px_rgba(51,47,58,0.06),inset_-1px_-1px_2px_rgba(255,255,255,0.9)]">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-tertiary text-[20px]">task_alt</span>
<span className="font-body-md text-body-md text-on-surface font-medium">City Maintenance Notified</span>
</div>
<span className="font-label-sm text-label-sm text-on-surface-variant">1 hr ago</span>
</div>
{/*  Action Button  */}
<button className="w-full py-3.5 rounded-DEFAULT bg-surface-container text-on-surface font-headline-sm text-headline-sm flex items-center justify-center gap-2 shadow-[4px_6px_12px_rgba(51,47,58,0.08),inset_2px_2px_3px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.05)] active:scale-[0.98] transition-all">
<span className="">VIEW INCIDENT</span>
<span className="material-symbols-outlined text-[20px]">arrow_forward</span>
</button>
</article>
</section>
{/*  Delightful Clay Empty State (Hidden by default, triggered by toggle below)  */}
<section className="hidden px-margin py-space-xl flex-col items-center justify-center text-center" id="empty-state-view">
<div className="w-28 h-28 rounded-full bg-surface-container-high flex items-center justify-center shadow-[8px_12px_20px_rgba(51,47,58,0.08),inset_3px_3px_6px_rgba(255,255,255,0.95),inset_-3px_-3px_6px_rgba(51,47,58,0.06)] mb-space-md relative">
<span className="material-symbols-outlined text-primary text-[52px]" >verified_user</span>
<div className="absolute -top-1 -right-1 w-8 h-8 rounded-full bg-secondary-container flex items-center justify-center text-on-secondary shadow-[0_4px_8px_rgba(218,38,118,0.4),inset_1px_1px_2px_rgba(255,255,255,0.6)]">
<span className="material-symbols-outlined text-[16px]">celebration</span>
</div>
</div>
<h3 className="font-headline-md text-headline-md text-on-surface font-bold">All Sectors All-Clear!</h3>
<p className="font-body-md text-body-md text-on-surface-variant max-w-xs mt-space-xs">
      No open hazards or unhandled citizen calls in your assigned quadrant right now. SafePath is synchronizing passively.
    </p>
<button className="mt-space-lg px-6 py-3 rounded-full bg-primary-container text-on-primary font-headline-sm text-headline-sm shadow-[0_10px_20px_rgba(124,58,237,0.35),inset_2px_2px_3px_rgba(255,255,255,0.4)] active:scale-95 transition-all" id="reset-feed-btn">
      Restore Operational Feed
    </button>
</section>
{/*  Interactive Prototype Simulation Control  */}
<aside className="px-margin mt-space-lg mb-space-md">
<div className="p-space-sm rounded-DEFAULT bg-surface-container shadow-[inset_2px_2px_4px_rgba(51,47,58,0.08),inset_-2px_-2px_4px_rgba(255,255,255,0.9)] flex items-center justify-between">
<div className="flex items-center gap-space-xs">
<span className="material-symbols-outlined text-secondary text-[20px]">science</span>
<span className="font-body-sm text-body-sm text-on-surface font-medium">Prototype Simulation Mode</span>
</div>
<button className="font-label-sm text-label-sm text-primary font-bold hover:underline flex items-center gap-0.5" id="simulate-zero-btn">
        Simulate Zero Incidents (Empty State) →
      </button>
</div>
</aside>
{/*  Sticky Thumb Zone Rapid SOS Trigger (Clay Volumetric Pill)  */}
<div className="sticky bottom-4 mx-margin z-20">
<div className="p-2 rounded-full bg-surface-container-lowest/80 backdrop-blur-md shadow-[0_10px_30px_rgba(51,47,58,0.12)] flex items-center justify-between gap-space-sm">
<div className="flex items-center gap-2 pl-3">
<span className="w-3 h-3 rounded-full bg-secondary-container shadow-[0_0_8px_rgba(218,38,118,0.8)] animate-pulse"></span>
<span className="font-label-sm text-label-sm font-bold text-on-surface tracking-tight uppercase">Squad Alfa • On-Duty</span>
</div>
<button className="px-5 py-2.5 rounded-full bg-secondary-container text-on-secondary-container font-headline-sm text-headline-sm flex items-center gap-1.5 shadow-[0_6px_16px_rgba(218,38,118,0.4),inset_2px_2px_3px_rgba(255,255,255,0.5),inset_-2px_-2px_3px_rgba(0,0,0,0.2)] active:scale-95 transition-all">
<span className="material-symbols-outlined text-[18px]">add_alert</span>
<span className="">BROADCAST SOS</span>
</button>
</div>
</div>
</div></>
  );
}

export default ResponseTeamIncidents;
