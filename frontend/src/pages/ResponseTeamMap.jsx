import { Link } from 'react-router-dom';

function ResponseTeamMap() {
  return (
    <><div className="flex flex-col w-full relative">
{/*  Ambient Atmospheric Blobs  */}
<div className="pointer-events-none absolute -top-10 -left-12 w-64 h-64 rounded-full bg-primary/10 blur-3xl -z-10"></div>
<div className="pointer-events-none absolute top-48 -right-10 w-72 h-72 rounded-full bg-tertiary-container/10 blur-3xl -z-10"></div>
{/*  Screen Header Strip  */}
<div className="px-margin pt-2 pb-space-sm flex flex-col gap-space-sm">
<div className="flex items-center justify-between gap-space-sm">
<div className="flex items-center gap-space-sm">
<button aria-label="Go back" className="w-11 h-11 rounded-full bg-surface-container flex items-center justify-center text-on-surface shadow-[6px_8px_16px_rgba(51,47,58,0.1),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.06)] active:scale-95 transition-transform" >
<span className="material-symbols-outlined text-[22px]">arrow_back</span>
</button>
<div className="flex flex-col">
<span className="font-headline-sm text-headline-sm text-on-surface tracking-tight">Incident Tactical Map</span>
<span className="font-label-sm text-label-sm text-on-surface-variant">Metro District 04 • Tactical Grid</span>
</div>
</div>
{/*  Live Mesh Status Bead  */}
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-high shadow-[3px_4px_8px_rgba(51,47,58,0.08),inset_1px_1px_2px_rgba(255,255,255,0.9)]">
<span className="w-2 h-2 rounded-full bg-secondary shadow-[0_0_8px_rgba(181,0,93,0.8)] animate-pulse"></span>
<span className="font-label-sm text-label-sm font-bold text-on-surface">LIVE FEED</span>
</div>
</div>
{/*  GPS Accuracy Clay Pill  */}
<div className="w-full flex items-center justify-between px-space-md py-2 rounded-full bg-surface-container-low shadow-[inset_2px_2px_4px_rgba(51,47,58,0.08),inset_-2px_-2px_4px_rgba(255,255,255,0.9)]">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-primary text-[18px]">satellite_alt</span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">GPS Active • <strong className="text-on-surface">2m Accuracy</strong></span>
</div>
<div className="flex items-center gap-1.5 bg-primary/10 px-2.5 py-0.5 rounded-full">
<span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
<span className="font-label-sm text-label-sm text-primary font-bold">Mesh Sync On</span>
</div>
</div>
</div>
{/*  Main Map Container  */}
<div className="relative px-margin w-full flex flex-col gap-space-md">
{/*  Map Canvas Card  */}
<div className="relative w-full h-[400px] rounded-lg overflow-hidden bg-surface-container shadow-[10px_18px_30px_-6px_rgba(51,47,58,0.12),inset_3px_3px_8px_rgba(255,255,255,0.9)] select-none" id="mapViewport">
{/*  Vector Map Graphics  */}
<svg className="absolute inset-0 w-full h-full" preserveaspectratio="none" viewbox="0 0 380 400" xmlns="http://www.w3.org/2000/svg">
<defs>
{/*  Water Fill Gradient  */}
<lineargradient id="waterGrad" x1="0" x2="1" y1="0" y2="1">
<stop offset="0%" stop-color="#c9e6ff" stop-opacity="0.85"></stop>
<stop offset="100%" stop-color="#89ceff" stop-opacity="0.95"></stop>
</lineargradient>
{/*  Safe Zone Gradient  */}
<lineargradient id="safeZoneGrad" x1="0" x2="1" y1="0" y2="1">
<stop offset="0%" stop-color="#10b981" stop-opacity="0.18"></stop>
<stop offset="100%" stop-color="#059669" stop-opacity="0.04"></stop>
</lineargradient>
{/*  Blocked Hazard Stripe Pattern  */}
<pattern height="8" id="blockedHatch" patterntransform="rotate(45 0 0)" patternunits="userSpaceOnUse" width="8">
<line stroke="#ba1a1a" stroke-opacity="0.8" stroke-width="4" x1="0" x2="0" y1="0" y2="8"></line>
<line stroke="#ffdad6" stroke-opacity="0.9" stroke-width="4" x1="4" x2="4" y1="0" y2="8"></line>
</pattern>
{/*  Tactical Grid Pattern  */}
<pattern height="30" id="tacticalGrid" patternunits="userSpaceOnUse" width="30">
<path d="M 30 0 L 0 0 0 30" fill="none" stroke="#ccc3d8" stroke-opacity="0.45" stroke-width="0.5"></path>
</pattern>
</defs>
{/*  Base Landmass  */}
<rect fill="#f3ebfa" height="400" width="380"></rect>
<rect fill="url(#tacticalGrid)" height="400" width="380"></rect>
{/*  River / Waterfront Curve  */}
<path d="M -10 60 C 90 80, 140 160, 120 280 C 110 330, 70 380, 40 410 L -10 410 Z" fill="url(#waterGrad)"></path>
<path d="M 0 62 C 95 82, 145 162, 125 282" fill="none" stroke="#ffffff" stroke-opacity="0.6" stroke-width="1.5"></path>
{/*  Waterfront Pier / Docks  */}
<path d="M 98 120 L 132 124 M 115 170 L 150 172 M 118 220 L 148 221" stroke="#89ceff" stroke-linecap="round" stroke-width="3"></path>
{/*  Safe Shelter Perimeter Zone  */}
<circle cx="60" cy="330" fill="url(#safeZoneGrad)" r="44" stroke="#10b981" stroke-dasharray="3,3" stroke-width="1.5"></circle>
{/*  Urban Street Grid Blocks  */}
<path d="M 140 30 L 390 30 M 140 85 L 390 85 M 140 145 L 390 145 M 140 210 L 390 210 M 140 280 L 390 280 M 140 350 L 390 350" stroke="#ede5f4" stroke-linecap="round" stroke-width="14"></path>
<path d="M 180 0 L 180 390 M 250 0 L 250 390 M 320 0 L 320 390" stroke="#ede5f4" stroke-width="14"></path>
{/*  Main Thoroughfare Arteries  */}
<path d="M 140 145 L 390 145" stroke="#ffffff" stroke-linecap="round" stroke-width="6"></path>
<path d="M 250 0 L 250 390" stroke="#ffffff" stroke-width="6"></path>
<path d="M 180 0 L 180 390" stroke="#ffffff" stroke-width="4"></path>
<path d="M 320 0 L 320 390" stroke="#ffffff" stroke-width="4"></path>
<path d="M 140 280 L 390 280" stroke="#ffffff" stroke-width="5"></path>
{/*  Blocked Road Segment (Pine St between 2nd & 3rd)  */}
<path d="M 185 210 L 245 210" stroke="url(#blockedHatch)" stroke-linecap="round" stroke-width="10"></path>
{/*  Tactical Response Route Vector (Bypassing blocked corridor)  */}
<path d="M 250 75 L 250 145 L 320 145 L 320 280 L 255 280" fill="none" id="routeCorridor" opacity="0.95" stroke="#7c3aed" stroke-dasharray="8,6" stroke-linecap="round" stroke-linejoin="round" stroke-width="5"></path>
{/*  Inner glow path  */}
<path d="M 250 75 L 250 145 L 320 145 L 320 280 L 255 280" fill="none" stroke="#ede0ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
{/*  River label  */}
<text fill="#005479" font-family="Nunito Sans" font-size="9" font-weight="700" letter-spacing="0.1em" opacity="0.6" transform="rotate(-70 35 180)" x="35" y="180">CANAL CORRIDOR</text>
{/*  Street labels  */}
<text fill="#7b7487" font-family="DM Sans" font-size="8" font-weight="600" x="256" y="25">4TH AVE</text>
<text fill="#7b7487" font-family="DM Sans" font-size="8" font-weight="600" x="326" y="25">5TH AVE</text>
<text fill="#7b7487" font-family="DM Sans" font-size="8" font-weight="600" x="330" y="140">PINE ST</text>
</svg>
{/*  Tactical Controls Floating Stack (Right)  */}
<div className="absolute right-3 top-3 flex flex-col gap-2 z-20">
<button aria-label="Zoom In" className="w-10 h-10 rounded-full bg-surface-container-lowest text-on-surface flex items-center justify-center shadow-[4px_6px_12px_rgba(51,47,58,0.12),inset_2px_2px_3px_rgba(255,255,255,0.9)] active:scale-90 transition-transform" id="zoomInBtn">
<span className="material-symbols-outlined text-[20px]">add</span>
</button>
<button aria-label="Zoom Out" className="w-10 h-10 rounded-full bg-surface-container-lowest text-on-surface flex items-center justify-center shadow-[4px_6px_12px_rgba(51,47,58,0.12),inset_2px_2px_3px_rgba(255,255,255,0.9)] active:scale-90 transition-transform" id="zoomOutBtn">
<span className="material-symbols-outlined text-[20px]">remove</span>
</button>
<button aria-label="Recenter GPS" className="w-10 h-10 rounded-full bg-surface-container-lowest text-primary flex items-center justify-center shadow-[4px_6px_12px_rgba(51,47,58,0.12),inset_2px_2px_3px_rgba(255,255,255,0.9)] active:scale-90 transition-transform" id="recenterGpsBtn">
<span className="material-symbols-outlined text-[20px]">my_location</span>
</button>
<button aria-label="Toggle Layers" className="w-10 h-10 rounded-full bg-surface-container-lowest text-on-surface-variant flex items-center justify-center shadow-[4px_6px_12px_rgba(51,47,58,0.12),inset_2px_2px_3px_rgba(255,255,255,0.9)] active:scale-90 transition-transform" id="layerToggleBtn">
<span className="material-symbols-outlined text-[20px]">layers</span>
</button>
</div>
{/*  MAP MARKER: Responder Location (Glowing Blue Beacon)  */}
<div className="absolute left-[236px] top-[60px] -translate-x-1/2 -translate-y-1/2 z-20 flex flex-col items-center pointer-events-auto cursor-pointer group">
{/*  Pulse Radar Rings  */}
<span className="absolute w-12 h-12 rounded-full bg-tertiary-fixed-dim/40 animate-ping"></span>
<span className="absolute w-8 h-8 rounded-full bg-tertiary-container/30"></span>
{/*  Clay Beacon Puck  */}
<div className="relative w-8 h-8 rounded-full bg-tertiary-container flex items-center justify-center shadow-[0_8px_16px_rgba(0,109,156,0.4),inset_2px_2px_4px_rgba(255,255,255,0.7),inset_-2px_-2px_4px_rgba(0,30,47,0.4)] text-on-primary">
<span className="material-symbols-outlined text-[18px] transform -rotate-45">navigation</span>
</div>
{/*  Direction Cone Marker  */}
<span className="mt-1 px-1.5 py-0.5 rounded-full bg-surface-container-lowest text-on-surface font-label-sm text-[10px] font-bold shadow-[2px_3px_6px_rgba(51,47,58,0.12)]">Unit 3 (You)</span>
</div>
{/*  MAP MARKER: Active Incident 1 (Flash Flood #INC-8924)  */}
<div className="absolute left-[242px] top-[278px] -translate-x-1/2 -translate-y-1/2 z-20 flex flex-col items-center cursor-pointer group">
{/*  Pulsing Warning Ring  */}
<span className="absolute w-14 h-14 rounded-full bg-secondary-container/40 animate-pulse"></span>
{/*  Clay Hazard Pill Badge  */}
<div className="relative px-2.5 py-1.5 rounded-full bg-secondary text-on-secondary flex items-center gap-1 shadow-[0_10px_20px_rgba(181,0,93,0.4),inset_2px_2px_4px_rgba(255,255,255,0.5),inset_-2px_-2px_4px_rgba(63,0,28,0.4)]">
<span className="material-symbols-outlined text-[16px]">tsunami</span>
<span className="font-label-sm text-[10px] font-extrabold uppercase">INC-8924</span>
</div>
{/*  Callout pointer  */}
<div className="w-2 h-2 rotate-45 -mt-1 bg-secondary"></div>
</div>
{/*  MAP MARKER: Active Incident 2 (Downed Wire - Pine St)  */}
<div className="absolute left-[200px] top-[140px] -translate-x-1/2 -translate-y-1/2 z-20 flex flex-col items-center">
<div className="relative w-7 h-7 rounded-full bg-amber-500 text-on-primary flex items-center justify-center shadow-[0_6px_14px_rgba(217,119,6,0.4),inset_2px_2px_3px_rgba(255,255,255,0.7),inset_-2px_-2px_3px_rgba(120,53,15,0.4)]">
<span className="material-symbols-outlined text-[15px]">electric_bolt</span>
</div>
<span className="mt-1 px-1.5 py-0.5 rounded-full bg-surface-container-lowest text-on-surface font-label-sm text-[9px] font-bold shadow-[2px_3px_6px_rgba(51,47,58,0.1)]">Wire Down</span>
</div>
{/*  MAP MARKER: Blocked Road Corridor Indicator  */}
<div className="absolute left-[214px] top-[208px] -translate-x-1/2 -translate-y-1/2 z-20 flex items-center gap-1 px-2 py-0.5 rounded-full bg-error text-on-error shadow-[0_4px_10px_rgba(186,26,26,0.35),inset_1px_1px_2px_rgba(255,255,255,0.6)]">
<span className="material-symbols-outlined text-[13px]">block</span>
<span className="font-label-sm text-[9px] font-bold">CLOSED</span>
</div>
{/*  MAP MARKER: Evacuation Shelter (Westlake Safe Shelter)  */}
<div className="absolute left-[60px] top-[320px] -translate-x-1/2 -translate-y-1/2 z-20 flex flex-col items-center cursor-pointer">
<div className="w-8 h-8 rounded-full bg-emerald-600 text-on-primary flex items-center justify-center shadow-[0_8px_16px_rgba(5,150,105,0.35),inset_2px_2px_4px_rgba(255,255,255,0.7),inset_-2px_-2px_4px_rgba(6,78,59,0.4)]">
<span className="material-symbols-outlined text-[18px]">security</span>
</div>
<div className="mt-1 px-2 py-0.5 rounded-full bg-surface-container-lowest text-on-surface font-label-sm text-[9px] font-bold whitespace-nowrap shadow-[2px_3px_6px_rgba(51,47,58,0.12)]">
          Westlake Shelter
        </div>
</div>
{/*  Map Overlaid Legend Card (Tactile Clay)  */}
<div className="absolute left-3 top-3 z-20 p-2.5 rounded-DEFAULT bg-surface-container-lowest/90 backdrop-blur-md shadow-[6px_10px_20px_rgba(51,47,58,0.1),inset_2px_2px_4px_rgba(255,255,255,0.9)] max-w-[150px]">
<span className="font-label-sm text-[10px] uppercase font-bold text-on-surface-variant tracking-wider block mb-1.5">Map Legend</span>
<div className="flex flex-col gap-1.5 font-label-sm text-[10px] text-on-surface">
<div className="flex items-center gap-1.5">
<span className="w-2.5 h-2.5 rounded-full bg-secondary shrink-0 shadow-[0_0_4px_rgba(181,0,93,0.6)]"></span>
<span className="truncate">Active Incident</span>
</div>
<div className="flex items-center gap-1.5">
<span className="w-2.5 h-2.5 rounded-full bg-tertiary-container shrink-0"></span>
<span className="truncate">Your Location</span>
</div>
<div className="flex items-center gap-1.5">
<span className="w-3.5 h-1.5 rounded-sm bg-error shrink-0"></span>
<span className="truncate">Blocked Corridor</span>
</div>
<div className="flex items-center gap-1.5">
<span className="w-2.5 h-2.5 rounded-full bg-emerald-600 shrink-0"></span>
<span className="truncate">Shelter Hub</span>
</div>
</div>
</div>
</div>
{/*  Active Route Status Info Strip  */}
<div className="w-full flex items-center justify-between px-space-md py-space-xs rounded-lg bg-surface-container shadow-[6px_10px_20px_rgba(51,47,58,0.06),inset_2px_2px_4px_rgba(255,255,255,0.8)]">
<div className="flex items-center gap-2">
<div className="w-7 h-7 rounded-full bg-primary-container text-on-primary flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.5)]">
<span className="material-symbols-outlined text-[16px]">alt_route</span>
</div>
<div className="flex flex-col">
<span className="font-label-sm text-label-sm text-on-surface font-bold">Safe Corridor Active</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">Detour via 5th Ave • Clear of water</span>
</div>
</div>
<span className="font-label-sm text-label-sm font-bold text-secondary uppercase bg-secondary-fixed px-2 py-0.5 rounded-full">High Priority</span>
</div>
{/*  Target Incident Focus Bottom Card  */}
<div className="w-full p-space-md rounded-lg bg-surface-container-lowest shadow-[10px_16px_28px_-4px_rgba(51,47,58,0.1),4px_6px_12px_-2px_rgba(124,58,237,0.05),inset_3px_3px_6px_rgba(255,255,255,0.9),inset_-3px_-3px_6px_rgba(51,47,58,0.04)] flex flex-col gap-space-md">
{/*  Incident Heading & Metrics  */}
<div className="flex items-start justify-between gap-space-sm">
<div className="flex items-start gap-space-sm">
<div className="w-11 h-11 rounded-DEFAULT bg-secondary-container/20 text-secondary flex items-center justify-center shadow-[inset_2px_2px_4px_rgba(218,38,118,0.15)] shrink-0">
<span className="material-symbols-outlined text-[24px]">crisis_alert</span>
</div>
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-1.5">
<span className="font-label-sm text-label-sm font-extrabold text-secondary uppercase">Level 3 Urgent</span>
<span className="w-1 h-1 rounded-full bg-outline-variant"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">Water Depth 0.8m</span>
</div>
<h3 className="font-title-md text-title-md text-on-surface font-bold truncate">Target: #INC-8924 (Flash Flood)</h3>
<p className="font-body-sm text-body-sm text-on-surface-variant truncate">4th Ave &amp; Pine St • 2 Civilians Sheltered</p>
</div>
</div>
</div>
{/*  Quick Metrics Recessed Wells  */}
<div className="grid grid-cols-2 gap-space-sm">
<div className="px-space-md py-space-sm rounded-DEFAULT bg-surface-container shadow-[inset_3px_3px_6px_rgba(51,47,58,0.08),inset_-2px_-2px_4px_rgba(255,255,255,0.9)] flex items-center gap-2">
<span className="material-symbols-outlined text-primary text-[20px]">near_me</span>
<div className="flex flex-col">
<span className="font-label-sm text-[10px] text-on-surface-variant uppercase font-bold">Distance</span>
<span className="font-headline-sm text-headline-sm text-on-surface font-extrabold leading-tight">1.2 km</span>
</div>
</div>
<div className="px-space-md py-space-sm rounded-DEFAULT bg-surface-container shadow-[inset_3px_3px_6px_rgba(51,47,58,0.08),inset_-2px_-2px_4px_rgba(255,255,255,0.9)] flex items-center gap-2">
<span className="material-symbols-outlined text-secondary text-[20px]">timer</span>
<div className="flex flex-col">
<span className="font-label-sm text-[10px] text-on-surface-variant uppercase font-bold">Rapid Route</span>
<span className="font-headline-sm text-headline-sm text-on-surface font-extrabold leading-tight">3 mins</span>
</div>
</div>
</div>
{/*  CTA Tactile Clay Buttons  */}
<div className="flex flex-col gap-space-xs pt-1">
{/*  Primary Action  */}
<button className="w-full h-12 rounded-DEFAULT bg-gradient-to-r from-primary-container to-primary text-on-primary font-headline-sm text-[15px] font-bold flex items-center justify-center gap-2 shadow-[0_12px_22px_-4px_rgba(124,58,237,0.38),inset_2px_2px_4px_rgba(255,255,255,0.45),inset_-2px_-2px_4px_rgba(0,0,0,0.2)] active:scale-[0.98] transition-all" id="dispatchBtn">
<span className="material-symbols-outlined text-[20px]">e911_emergency</span>
<span>START RAPID DISPATCH</span>
</button>
{/*  Secondary Action  */}
<button className="w-full h-11 rounded-DEFAULT bg-surface-container text-on-surface font-headline-sm text-[14px] font-bold flex items-center justify-center gap-2 shadow-[4px_6px_12px_rgba(51,47,58,0.08),inset_2px_2px_3px_rgba(255,255,255,0.9),inset_-2px_-2px_3px_rgba(51,47,58,0.04)] active:scale-[0.98] transition-all" id="detailsBtn">
<span className="material-symbols-outlined text-[18px]">info</span>
<span>VIEW INCIDENT DETAILS</span>
</button>
</div>
</div>
</div>
{/*  Interactive Map Client Behavior Script  */}

</div></>
  );
}

export default ResponseTeamMap;
