import { Link } from 'react-router-dom';

function CitizenMap() {
  return (
    <><div className="flex flex-col w-full relative select-none">
{/*  Soft Ambient Backlight Glow  */}
<div className="absolute -top-10 left-1/2 -translate-x-1/2 w-80 h-44 bg-primary-fixed-dim/35 rounded-full blur-3xl pointer-events-none -z-10"></div>
{/*  Operational Header Context Bar  */}
<div className="flex items-center justify-between gap-space-sm mb-space-md">
<div className="flex items-center gap-space-sm">
<a className="w-11 h-11 min-w-[44px] min-h-[44px] rounded-full bg-surface-container clay-card flex items-center justify-center text-on-surface hover:text-primary active:scale-95 transition-all" data-path="home-citizen-dashboard" href="#">
<span className="material-symbols-outlined text-[20px]">arrow_back</span>
</a>
<div className="flex flex-col">
<h2 className="font-headline-sm text-headline-sm text-on-surface font-bold">My Map</h2>
<span className="font-label-sm text-label-sm text-on-surface-variant flex items-center gap-1">
<span className="w-1.5 h-1.5 rounded-full bg-tertiary-container animate-pulse"></span>
          Live Tactical Layer
        </span>
</div>
</div>
{/*  GPS Accuracy Clay Badge  */}
<div className="flex items-center gap-1.5 py-1 px-3 rounded-full bg-surface-container-lowest clay-card text-on-surface-variant shadow-sm">
<span className="material-symbols-outlined text-[16px] text-tertiary-container" >my_location</span>
<span className="font-label-sm text-label-sm text-on-surface font-semibold tracking-tight">GPS High Accuracy</span>
</div>
</div>
{/*  Interactive Map Canvas Container (Clay Card Framed)  */}
<div className="relative w-full rounded-3xl bg-surface-container-lowest clay-card overflow-hidden h-[420px] mb-space-md">
{/*  Map Background Engine / Data Hook  */}
<div className="absolute inset-0 w-full h-full bg-surface-container-high bg-cover bg-center" data-location="9th and Pine Street, Seattle" >
{/*  Topographical & Tactical Clay SVG Overlay  */}
<svg className="absolute inset-0 w-full h-full pointer-events-none" preserveaspectratio="none" viewbox="0 0 400 420" xmlns="http://www.w3.org/2000/svg">
<defs>
<lineargradient id="safeZoneGrad" x1="0" x2="1" y1="0" y2="1">
<stop offset="0%" stop-color="#10B981" stop-opacity="0.32"></stop>
<stop offset="100%" stop-color="#059669" stop-opacity="0.14"></stop>
</lineargradient>
<lineargradient id="floodZoneGrad" x1="0" x2="0" y1="0" y2="1">
<stop offset="0%" stop-color="#F59E0B" stop-opacity="0.28"></stop>
<stop offset="100%" stop-color="#D97706" stop-opacity="0.08"></stop>
</lineargradient>
<filter height="140%" id="softGlow" width="140%" x="-20%" y="-20%">
<fegaussianblur result="blur" stddeviation="3"></fegaussianblur>
<fecomposite in="SourceGraphic" in2="blur" operator="over"></fecomposite>
</filter>
</defs>
{/*  Elevation / River Feature  */}
<path d="M-20,120 Q60,180 140,160 T320,240 T440,290" fill="none" opacity="0.45" stroke="#89CEFF" stroke-linecap="round" stroke-width="14"></path>
<path d="M-20,120 Q60,180 140,160 T320,240 T440,290" fill="none" opacity="0.75" stroke="#006D9C" stroke-dasharray="6 4" stroke-width="3"></path>
{/*  Road Network Representation  */}
<path d="M40,0 L70,420 M180,0 L200,420 M310,0 L330,420 M0,90 L400,105 M0,220 L400,230 M0,330 L400,340" fill="none" opacity="0.8" stroke="#E7E0EE" stroke-linecap="round" stroke-width="6"></path>
<path d="M40,0 L70,420 M180,0 L200,420 M310,0 L330,420 M0,90 L400,105 M0,220 L400,230 M0,330 L400,340" fill="none" opacity="0.9" stroke="#FFFFFF" stroke-linecap="round" stroke-width="2"></path>
{/*  Emerald Safe Zone Polygon  */}
<polygon fill="url(#safeZoneGrad)" points="120,40 240,30 260,110 135,120" stroke="#10B981" stroke-dasharray="4 2" stroke-width="2"></polygon>
{/*  Flooding Influence Radius  */}
<circle cx="285" cy="180" fill="url(#floodZoneGrad)" r="42" stroke="#F59E0B" stroke-dasharray="3 3" stroke-width="1.5"></circle>
</svg>
</div>
{/*  Active Incident Clay Marker: Emerald Shelter Area  */}
<div className="absolute top-10 left-28 -translate-x-1/2 flex flex-col items-center pointer-events-auto cursor-pointer group active:scale-95 transition-transform" id="shelterMarker">
<div className="px-2.5 py-1 rounded-full bg-surface-container-lowest clay-card text-on-surface flex items-center gap-1 shadow-sm mb-1">
<span className="w-2 h-2 rounded-full bg-emerald-500"></span>
<span className="font-label-sm text-label-sm font-bold">Central Arena Shelter</span>
</div>
<div className="w-8 h-8 rounded-full bg-emerald-500 text-surface-container-lowest flex items-center justify-center clay-pop shadow-md shadow-emerald-500/30">
<span className="material-symbols-outlined text-[18px]" >night_shelter</span>
</div>
</div>
{/*  Active Incident Clay Marker: Flooding Amber  */}
<div className="absolute top-36 right-8 flex flex-col items-center pointer-events-auto cursor-pointer active:scale-95 transition-transform" id="floodMarker">
<div className="px-2.5 py-1 rounded-full bg-surface-container-lowest clay-card text-on-surface flex items-center gap-1 shadow-sm mb-1">
<span className="material-symbols-outlined text-[14px] text-amber-500" >warning</span>
<span className="font-label-sm text-label-sm font-bold">Flooding (1.2 km)</span>
</div>
<div className="w-8 h-8 rounded-full bg-amber-500 text-surface-container-lowest flex items-center justify-center clay-pop shadow-md shadow-amber-500/30 animate-bounce">
<span className="material-symbols-outlined text-[17px]">water_damage</span>
</div>
</div>
{/*  Active Incident Clay Marker: Road Blocked Red  */}
<div className="absolute bottom-28 left-12 flex flex-col items-center pointer-events-auto cursor-pointer active:scale-95 transition-transform" id="blockMarker">
<div className="px-2.5 py-1 rounded-full bg-surface-container-lowest clay-card text-on-surface flex items-center gap-1 shadow-sm mb-1">
<span className="w-2 h-2 rounded-full bg-error"></span>
<span className="font-label-sm text-label-sm font-bold">Tree Down • Elm St</span>
</div>
<div className="w-8 h-8 rounded-full bg-error text-surface-container-lowest flex items-center justify-center clay-pop shadow-md shadow-error/30">
<span className="material-symbols-outlined text-[17px]">block</span>
</div>
</div>
{/*  Blue Pulsing "Your Location" Clay Pin (9th & Pine)  */}
<div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center pointer-events-none" id="userLocationPin">
{/*  Radar Pulse Waves  */}
<div className="relative flex items-center justify-center">
<span className="absolute w-14 h-14 rounded-full bg-tertiary-container/20 animate-ping"></span>
<span className="absolute w-9 h-9 rounded-full bg-tertiary-fixed-dim/40"></span>
<div className="w-6 h-6 rounded-full bg-tertiary-container text-surface-container-lowest flex items-center justify-center clay-pop shadow-lg shadow-tertiary-container/40">
<div className="w-2.5 h-2.5 rounded-full bg-surface-container-lowest"></div>
</div>
</div>
<div className="mt-1 px-2.5 py-0.5 rounded-full bg-surface-container-lowest/90 backdrop-blur-md clay-card">
<span className="font-label-sm text-label-sm text-on-surface font-extrabold tracking-tight">You (9th &amp; Pine)</span>
</div>
</div>
{/*  Floating Map Controls (Right Dock)  */}
<div className="absolute top-4 right-4 flex flex-col gap-2 pointer-events-auto">
<button aria-label="Zoom in" className="w-11 h-11 rounded-full bg-surface-container-lowest/95 backdrop-blur-md clay-card flex items-center justify-center text-on-surface hover:text-primary active:scale-90 transition-transform" id="zoomInBtn" type="button">
<span className="material-symbols-outlined text-[20px]">add</span>
</button>
<button aria-label="Zoom out" className="w-11 h-11 rounded-full bg-surface-container-lowest/95 backdrop-blur-md clay-card flex items-center justify-center text-on-surface hover:text-primary active:scale-90 transition-transform" id="zoomOutBtn" type="button">
<span className="material-symbols-outlined text-[20px]">remove</span>
</button>
<button aria-label="Recenter GPS" className="w-11 h-11 rounded-full bg-surface-container-lowest/95 backdrop-blur-md clay-card flex items-center justify-center text-tertiary-container hover:text-primary active:scale-90 transition-transform shadow-sm" id="recenterBtn" type="button">
<span className="material-symbols-outlined text-[20px]" >near_me</span>
</button>
</div>
{/*  Map Legend Clay Card (Bottom Left Dock)  */}
<div className="absolute bottom-3 left-3 bg-surface-container-lowest/95 backdrop-blur-md p-2.5 rounded-2xl clay-card flex flex-col gap-1.5 pointer-events-auto">
<div className="flex items-center gap-2">
<span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-xs"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Safe Shelter</span>
</div>
<div className="flex items-center gap-2">
<span className="w-2.5 h-2.5 rounded-[2px] rotate-45 bg-amber-500"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Caution Hazard</span>
</div>
<div className="flex items-center gap-2">
<span className="w-2.5 h-2.5 rounded-full bg-error"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Blocked Road</span>
</div>
<div className="flex items-center gap-2">
<span className="w-2.5 h-2.5 rounded-full bg-tertiary-container ring-2 ring-tertiary-fixed-dim"></span>
<span className="font-label-sm text-label-sm text-on-surface font-semibold">Your Location</span>
</div>
</div>
</div>
{/*  Interactive Tactical Safe Route Recommendation Card  */}
<div className="w-full bg-surface-container-lowest rounded-3xl p-space-md clay-card relative overflow-hidden">
<div className="absolute -right-6 -bottom-6 w-28 h-28 bg-primary-fixed/40 rounded-full blur-2xl pointer-events-none"></div>
<div className="flex items-start justify-between gap-space-sm mb-space-sm">
<div className="flex items-center gap-2.5">
<div className="w-10 h-10 rounded-2xl bg-primary-fixed flex items-center justify-center text-primary clay-card shrink-0">
<span className="material-symbols-outlined text-[22px]">alt_route</span>
</div>
<div>
<span className="font-label-sm text-label-sm text-secondary font-bold uppercase tracking-wider">Dynamic Evacuation</span>
<h3 className="font-headline-sm text-headline-sm text-on-surface font-bold">Need a safer route?</h3>
</div>
</div>
<div className="px-2 py-0.5 rounded-full bg-surface-container font-label-sm text-label-sm text-on-surface-variant font-medium">
        Live Analysis
      </div>
</div>
<p className="font-body-md text-body-md text-on-surface-variant mb-space-md">
      Calculate the verified safest corridor avoiding active flood sectors and fallen tree obstructions on Elm Street.
    </p>
{/*  Route Stats Preview Chips  */}
<div className="grid grid-cols-2 gap-space-sm mb-space-md">
<div className="p-2.5 rounded-2xl bg-surface-container-low clay-card flex items-center gap-2">
<span className="material-symbols-outlined text-[20px] text-tertiary-container">schedule</span>
<div className="flex flex-col">
<span className="font-label-sm text-label-sm text-on-surface-variant">Estimated</span>
<span className="font-title-md text-title-md text-on-surface font-bold">14 min walk</span>
</div>
</div>
<div className="p-2.5 rounded-2xl bg-surface-container-low clay-card flex items-center gap-2">
<span className="material-symbols-outlined text-[20px] text-emerald-600">verified_user</span>
<div className="flex flex-col">
<span className="font-label-sm text-label-sm text-on-surface-variant">Shelter Clearance</span>
<span className="font-title-md text-title-md text-on-surface font-bold">100% Verified</span>
</div>
</div>
</div>
{/*  Primary Action Raised Clay Button  */}
<a className="w-full min-h-[52px] py-3.5 px-space-md rounded-2xl bg-gradient-to-r from-[#A78BFA] to-[#7C3AED] text-on-primary font-headline-sm text-headline-sm flex items-center justify-center gap-2 clay-pop active:scale-[0.98] transition-transform" data-path="safe-route-guidance" href="#" id="findSafeRouteTrigger">
<span className="material-symbols-outlined text-[22px]">explore</span>
<span>Find Safe Route</span>
</a>
</div>
{/*  Interactive Map Client Behavior Script  */}

</div></>
  );
}

export default CitizenMap;
