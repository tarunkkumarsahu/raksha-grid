import { Link } from 'react-router-dom';

function SafeRoute() {
  return (
    <><div className="flex flex-col w-full pb-8 space-y-space-md">
{/*  Mesh Satellite Network Status Micro-Bead  */}
<div className="flex items-center justify-between px-space-xs">
<div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container clay-card">
<span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse shadow-sm"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium tracking-wide uppercase">Offline Mesh Active • 14 Nodes</span>
</div>
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-low text-tertiary font-label-sm text-label-sm">
<span className="material-symbols-outlined text-[16px]">verified</span>
<span>Live Civil Defense Feed</span>
</div>
</div>
{/*  Routing Waypoints Clay Card  */}
<div className="w-full bg-surface-container-lowest rounded-xl p-space-md clay-card flex flex-col gap-space-sm relative overflow-hidden">
{/*  Subtle Ambient Glow  */}
<div className="absolute -top-12 -right-12 w-32 h-32 bg-primary-fixed/20 rounded-full blur-2xl pointer-events-none"></div>
<div className="relative flex flex-col gap-3">
{/*  Origin Field  */}
<div className="flex items-center gap-3">
<div className="flex flex-col items-center">
<div className="w-7 h-7 rounded-full bg-tertiary-fixed flex items-center justify-center shadow-inner">
<span className="w-2.5 h-2.5 rounded-full bg-tertiary shadow-sm"></span>
</div>
<div className="w-0.5 h-7 bg-outline-variant/60 my-0.5 border-dashed"></div>
</div>
<div className="flex-1">
<label className="font-label-sm text-label-sm text-outline uppercase tracking-wider block mb-0.5">Start Point</label>
<div className="w-full bg-surface-container-low rounded-lg px-3.5 py-2.5 flex items-center justify-between shadow-inner">
<span className="font-body-md text-body-md text-on-surface font-medium truncate">Current Location (Downtown Precinct)</span>
<span className="material-symbols-outlined text-outline text-[18px]">my_location</span>
</div>
</div>
</div>
{/*  Destination Field  */}
<div className="flex items-center gap-3">
<div className="w-7 h-7 rounded-full bg-emerald-100 flex items-center justify-center shadow-inner">
<span className="material-symbols-outlined text-emerald-600 text-[18px]">location_on</span>
</div>
<div className="flex-1">
<label className="font-label-sm text-label-sm text-outline uppercase tracking-wider block mb-0.5">Destination</label>
<div className="w-full bg-surface-container-low rounded-lg px-3.5 py-2 flex items-center justify-between shadow-inner focus-within:ring-2 focus-within:ring-primary/20">
<input className="bg-transparent border-0 outline-none w-full font-body-md text-body-md text-on-surface font-semibold text-ellipsis" type="text" value="Westlake Emergency Shelter"/>
<button className="w-6 h-6 flex items-center justify-center rounded-full bg-surface-container text-outline hover:text-on-surface" type="button">
<span className="material-symbols-outlined text-[16px]">edit</span>
</button>
</div>
</div>
</div>
</div>
</div>
{/*  Interactive Route Map Preview  */}
<div className="w-full bg-surface-container-low rounded-xl p-space-xs clay-card flex flex-col overflow-hidden">
<div className="relative w-full h-56 rounded-lg overflow-hidden bg-surface-container-highest flex items-center justify-center">
{/*  Simulated Vector Map Graphic  */}
<svg className="absolute inset-0 w-full h-full" fill="none" viewbox="0 0 360 224" xmlns="http://www.w3.org/2000/svg">
{/*  City Grid Background Pattern  */}
<path d="M-20 40H380 M-20 90H380 M-20 140H380 M-20 190H380" stroke="#DDD4E8" stroke-linecap="round" stroke-width="2"></path>
<path d="M50 -20V240 M120 -20V240 M210 -20V240 M290 -20V240" stroke="#DDD4E8" stroke-linecap="round" stroke-width="2"></path>
{/*  Water Body / Flood Threat Zone  */}
<ellipse cx="165" cy="115" fill="#DA2676" fill-opacity="0.16" rx="55" ry="34"></ellipse>
<ellipse cx="165" cy="115" fill="#DA2676" fill-opacity="0.22" rx="42" ry="24"></ellipse>
{/*  Avoided Red Blocked Path  */}
<path d="M65 170L135 125L175 110L230 65" stroke="#BA1A1A" stroke-dasharray="6 6" stroke-linecap="round" stroke-width="3.5"></path>
{/*  Safe Path (Glow underlay + Emerald Path)  */}
<path d="M65 170L85 140L100 80L160 55L245 55L290 60" opacity="0.3" stroke="#10B981" stroke-linecap="round" stroke-linejoin="round" stroke-width="9"></path>
<path d="M65 170L85 140L100 80L160 55L245 55L290 60" stroke="#10B981" stroke-linecap="round" stroke-linejoin="round" stroke-width="4.5"></path>
{/*  Alternate Route (Dotted Lilac)  */}
<path d="M65 170L110 195L210 195L270 140L290 60" opacity="0.6" stroke="#7C3AED" stroke-dasharray="4 4" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"></path>
{/*  Origin Dot Marker  */}
<circle cx="65" cy="170" fill="#005479" r="9"></circle>
<circle cx="65" cy="170" fill="#FFFFFF" r="4"></circle>
{/*  Destination Marker Pin  */}
<g transform="translate(280, 42)">
<circle cx="10" cy="10" fill="#10B981" r="10"></circle>
<path d="M10 5L6 9H8V14H12V9H14L10 5Z" fill="#FFFFFF"></path>
</g>
</svg>
{/*  Map Overlay Badges  */}
<div className="absolute top-2.5 left-2.5 flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container-lowest/90 backdrop-blur-md shadow-sm">
<span className="w-2 h-2 rounded-full bg-emerald-500"></span>
<span className="font-label-sm text-label-sm font-bold text-on-surface">Route Clear</span>
</div>
{/*  Hazard Bypass Pill  */}
<div className="absolute bottom-2.5 right-2.5 flex items-center gap-1.5 px-3 py-1 rounded-full bg-error-container/90 backdrop-blur-md shadow-sm text-on-error-container">
<span className="material-symbols-outlined text-[15px]">water_damage</span>
<span className="font-label-sm text-label-sm font-semibold">4th Ave Flooded</span>
</div>
{/*  Quick Zoom Tactile Buttons  */}
<div className="absolute right-2.5 top-2.5 flex flex-col gap-1.5">
<button aria-label="Zoom In" className="w-8 h-8 rounded-full bg-surface-container-lowest flex items-center justify-center text-on-surface clay-card active:scale-95 transition-transform" type="button">
<span className="material-symbols-outlined text-[18px]">add</span>
</button>
<button aria-label="Zoom Out" className="w-8 h-8 rounded-full bg-surface-container-lowest flex items-center justify-center text-on-surface clay-card active:scale-95 transition-transform" type="button">
<span className="material-symbols-outlined text-[18px]">remove</span>
</button>
</div>
</div>
<div className="px-space-sm py-2 flex items-center justify-between text-outline">
<span className="font-label-sm text-label-sm flex items-center gap-1">
<span className="material-symbols-outlined text-[14px]">tune</span> Elevation stable (+8m)
      </span>
<span className="font-label-sm text-label-sm flex items-center gap-1">
<span className="material-symbols-outlined text-[14px]">cell_tower</span> Full 5G coverage
      </span>
</div>
</div>
{/*  Route Summary Clay Cards  */}
<div className="flex flex-col space-y-3">
{/*  Primary Option: Recommended Safe Route  */}
<div className="w-full bg-surface-container-lowest rounded-xl p-space-md clay-card relative cursor-pointer border-0 active:scale-[0.99] transition-transform">
<div className="flex items-start justify-between gap-2 mb-2">
<div className="flex items-center gap-2">
<div className="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center">
<span className="material-symbols-outlined text-emerald-600 text-[18px]">verified_user</span>
</div>
<span className="font-title-md text-title-md text-on-surface font-bold">Recommended Safe Route</span>
</div>
<span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-label-sm text-label-sm font-bold flex items-center gap-1">
<span className="material-symbols-outlined text-[13px]">check_circle</span>
          Safest Route
        </span>
</div>
{/*  Quick Metrics Grid  */}
<div className="grid grid-cols-3 gap-2 my-space-sm bg-surface-container-low rounded-lg p-2.5">
<div className="flex flex-col">
<span className="font-label-sm text-label-sm text-outline">Time</span>
<span className="font-headline-sm text-headline-sm text-on-surface font-extrabold">18 <span className="font-body-md text-body-md font-semibold text-outline">min</span></span>
</div>
<div className="flex flex-col">
<span className="font-label-sm text-label-sm text-outline">Distance</span>
<span className="font-headline-sm text-headline-sm text-on-surface font-extrabold">6.4 <span className="font-body-md text-body-md font-semibold text-outline">km</span></span>
</div>
<div className="flex flex-col">
<span className="font-label-sm text-label-sm text-outline">Condition</span>
<span className="font-label-lg text-label-lg text-emerald-600 font-bold truncate">100% Safe</span>
</div>
</div>
{/*  Hazard Mitigation Note  */}
<div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-container text-on-surface-variant font-body-sm text-body-sm">
<span className="material-symbols-outlined text-[17px] text-secondary">turn_right</span>
<span>Bypasses 4th Ave flash flood zone (<span className="font-semibold text-on-surface">+3 mins</span>)</span>
</div>
</div>
{/*  Alternative Option: Route B  */}
<div className="w-full bg-surface-container rounded-xl p-space-md clay-card cursor-pointer hover:bg-surface-container-high transition-colors active:scale-[0.99]">
<div className="flex items-center justify-between mb-1.5">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-outline text-[20px]">alt_route</span>
<span className="font-title-md text-title-md text-on-surface font-bold">Route B via Skyline Blvd</span>
</div>
<span className="px-2 py-0.5 rounded-full bg-surface-container-highest text-on-surface-variant font-label-sm text-label-sm font-semibold">Low Hazard</span>
</div>
<div className="flex items-center gap-4 text-on-surface-variant font-body-md text-body-md">
<span><strong className="text-on-surface">24</strong> min</span>
<span>•</span>
<span><strong className="text-on-surface">7.8</strong> km</span>
<span>•</span>
<span className="text-outline">Moderate debris reported</span>
</div>
</div>
</div>
{/*  Actions Cluster  */}
<div className="flex flex-col space-y-3 pt-2">
{/*  Start Navigation Button  */}
<button className="w-full min-h-[54px] rounded-lg bg-gradient-to-r from-[#A78BFA] to-[#7C3AED] text-on-primary font-headline-sm text-headline-sm font-bold flex items-center justify-center gap-2 clay-pop active:scale-[0.98] transition-all" type="button">
<span className="material-symbols-outlined text-[24px]">navigation</span>
<span>START NAVIGATION</span>
</button>
{/*  Error State Simulation Trigger  */}
<button className="w-full py-2.5 text-center text-primary font-label-md text-label-md font-semibold hover:underline flex items-center justify-center gap-1" id="toggle-unavailable-btn" type="button">
<span>Simulate No Route Available</span>
<span className="material-symbols-outlined text-[16px]">arrow_forward</span>
</button>
</div>
{/*  Conditional Modal / Drawer for "No Route Available"  */}
<div className="hidden fixed inset-x-4 bottom-8 z-50 p-space-md rounded-xl bg-surface-container-lowest clay-card shadow-2xl flex flex-col gap-3" id="no-route-modal">
<div className="flex items-center justify-between">
<div className="flex items-center gap-2 text-error">
<span className="material-symbols-outlined text-[24px]">crisis_alert</span>
<h2 className="font-headline-sm text-headline-sm font-bold">All Direct Routes Cut Off</h2>
</div>
<button className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center text-outline hover:text-on-surface" id="close-modal-btn" type="button">
<span className="material-symbols-outlined text-[18px]">close</span>
</button>
</div>
<p className="font-body-md text-body-md text-on-surface-variant">
      Flash flooding and collapsed branches currently impassable between Downtown Precinct and Westlake.
    </p>
<div className="p-3 bg-error-container/40 rounded-lg flex items-center gap-2 text-on-error-container font-label-md text-label-md">
<span className="material-symbols-outlined text-[20px]">flip_camera_ios</span>
<span>Recommended: Seek nearest vertical refuge at <strong>Grand Plaza 4F</strong> (150m away).</span>
</div>
<button className="w-full min-h-[46px] rounded-lg bg-secondary text-on-secondary font-label-lg text-label-lg font-bold flex items-center justify-center gap-2 shadow-md" type="button">
<span className="material-symbols-outlined text-[20px]">sos</span>
      Request Evacuation Escort
    </button>
</div>
</div></>
  );
}

export default SafeRoute;
