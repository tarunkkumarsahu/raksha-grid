import { Link } from 'react-router-dom';

function CitizenDashboard() {
  return (
    <><div className="flex flex-col w-full gap-space-lg select-none">
{/*  Soft Ambient Glow Underlay  */}
<div className="relative">
<div className="absolute -top-10 left-1/2 -translate-x-1/2 w-72 h-44 bg-primary-fixed-dim/35 rounded-full blur-3xl pointer-events-none -z-10"></div>
<div className="absolute top-24 -right-8 w-48 h-48 bg-secondary-fixed/30 rounded-full blur-2xl pointer-events-none -z-10"></div>
{/*  User Warm Welcome & Subtitle  */}
<div className="flex items-center justify-between gap-space-md mb-space-sm pt-space-xs">
<div className="flex flex-col">
<div className="flex items-center gap-space-xs">
<h2 className="font-headline-lg text-headline-lg text-on-surface font-extrabold tracking-tight">Hello, Sarah!</h2>
<span className="text-2xl animate-bounce">👋</span>
</div>
<p className="font-body-md text-body-md text-on-surface-variant flex items-center gap-1 mt-0.5">
<span className="material-symbols-outlined text-[16px] text-primary">location_on</span>
<span className="">Downtown Precinct • Safe Zone</span>
</p>
</div>
{/*  Quick Mesh/GPS Status Clay Pill  */}
<div className="clay-card px-3 py-1.5 rounded-full bg-surface-container-lowest flex items-center gap-1.5 shadow-sm">
<span className="relative flex h-2.5 w-2.5">
<span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
<span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
</span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-bold tracking-wide">MESH ON</span>
</div>
</div>
{/*  MAIN SAFETY STATUS CLAY CARD  */}
<section className="relative rounded-3xl p-6 bg-gradient-to-br from-emerald-50 via-surface-container-lowest to-emerald-100/40 clay-card overflow-hidden transition-all duration-300" id="safetyCard">
{/*  Background subtle clay glow sphere  */}
<div className="absolute -right-10 -bottom-10 w-44 h-44 bg-emerald-200/40 rounded-full blur-xl pointer-events-none"></div>
<div className="flex items-start justify-between relative z-10">
{/*  3D Tactile Shield Badge  */}
<div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 p-0.5 clay-pop flex items-center justify-center text-on-primary">
<div className="w-full h-full rounded-[14px] bg-emerald-500/90 flex items-center justify-center">
<span className="material-symbols-outlined text-[36px]" >verified_user</span>
</div>
</div>
{/*  Pill Status Indicator  */}
<div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 shadow-sm">
<span className="w-2 h-2 rounded-full bg-emerald-500"></span>
<span className="font-label-sm text-label-sm font-bold uppercase tracking-wider">Perimeter Clear</span>
</div>
</div>
<div className="mt-4 relative z-10">
<div className="flex items-baseline gap-2">
<h3 className="font-display-lg-mobile text-display-lg-mobile font-extrabold text-emerald-950 tracking-tight">YOU'RE SAFE</h3>
</div>
<p className="font-body-md text-body-md text-on-surface-variant mt-1 max-w-[90%]">
          No severe hazards or active emergencies reported within <strong className="text-on-surface font-semibold">5 km</strong> of your coordinates.
        </p>
</div>
{/*  Live GPS & Offline Sync details  */}
<div className="mt-4 pt-3.5 flex items-center justify-between text-on-surface-variant text-label-sm font-label-md">
<span className="flex items-center gap-1.5 text-emerald-900 font-semibold">
<span className="material-symbols-outlined text-[15px] text-emerald-600">satellite_alt</span>
          Updated 2 mins ago • GPS Active
        </span>
<span className="text-on-surface-variant/70">Grid #44-B</span>
</div>
{/*  Quick Status Switcher (Delightful Clay Toggle Bar)  */}
<div className="mt-4 pt-2 flex items-center gap-2">
<button className="flex-1 min-h-[46px] rounded-2xl bg-surface-container-lowest text-on-surface font-label-md text-label-md font-bold clay-card flex items-center justify-center gap-2 hover:bg-surface-container-low active:scale-95 transition-transform" id="sosPromptBtn" type="button">
<span className="material-symbols-outlined text-[18px] text-secondary">help</span>
<span className="">I Need Help</span>
</button>
<button className="w-12 h-[46px] rounded-2xl bg-surface-container-high text-on-surface-variant font-label-md clay-card flex items-center justify-center hover:text-primary active:scale-95 transition-all" id="broadcastStatusBtn" type="button">
<span className="material-symbols-outlined text-[20px]">share_location</span>
</button>
</div>
</section>
</div>
{/*  LIVE HAZARD MAP PREVIEW SECTION  */}
<section className="flex flex-col gap-space-sm">
<div className="flex items-center justify-between px-1">
<div className="flex items-center gap-2">
<div className="w-2.5 h-2.5 rounded-full bg-primary animate-pulse"></div>
<h3 className="font-title-md text-title-md text-on-surface font-bold tracking-tight">Your Area Live Map</h3>
</div>
<a className="font-label-md text-label-md text-primary font-bold hover:underline flex items-center" data-path="live-hazard-map" href="#">
        Full Radar
        <span className="material-symbols-outlined text-[16px] ml-0.5">chevron_right</span>
</a>
</div>
{/*  Map Preview Canvas with Clay Relief  */}
<div className="relative w-full h-56 rounded-3xl overflow-hidden clay-card bg-surface-container-high group">
{/*  Static Location View Container  */}
<div className="w-full h-full bg-cover bg-center"  data-location="Seattle Downtown 4th Ave and Pine" ></div>
{/*  Map Gradient Vignette for Readability  */}
<div className="absolute inset-0 bg-gradient-to-t from-inverse-surface/60 via-transparent to-transparent pointer-events-none"></div>
{/*  Pulsing User Location Beacon  */}
<div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center justify-center pointer-events-none">
<div className="w-12 h-12 rounded-full bg-primary/20 animate-ping absolute"></div>
<div className="w-8 h-8 rounded-full bg-primary/40 flex items-center justify-center">
<div className="w-4 h-4 rounded-full bg-primary shadow-lg ring-4 ring-surface-container-lowest"></div>
</div>
</div>
{/*  Flooding Hazard Clay Pin  */}
<div className="absolute top-8 right-12 flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-500/95 text-on-primary clay-pop text-label-sm font-label-sm backdrop-blur-sm">
<span className="material-symbols-outlined text-[14px]">water_damage</span>
<span className="">Flooding 1.2km</span>
</div>
{/*  Safe Sanctuary Pin  */}
<div className="absolute bottom-6 left-5 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-lowest/90 text-on-surface clay-card text-label-sm font-label-md backdrop-blur-md">
<span className="material-symbols-outlined text-[16px] text-emerald-600" >health_and_safety</span>
<span className="font-bold">Westlake Shelter (Open)</span>
</div>
{/*  Compact Compass Chip  */}
<div className="absolute top-4 left-4 w-9 h-9 rounded-2xl bg-surface-container-lowest/90 backdrop-blur-md clay-card flex items-center justify-center text-primary">
<span className="material-symbols-outlined text-[20px]">explore</span>
</div>
</div>
{/*  Quick Navigation Action Trio  */}
<div className="grid grid-cols-3 gap-space-sm pt-1">
<a className="min-h-[52px] rounded-2xl bg-surface-container-low text-on-surface hover:bg-surface-container clay-card p-2 flex flex-col items-center justify-center gap-0.5 text-center active:scale-95 transition-all" data-path="live-hazard-map" href="#">
<span className="material-symbols-outlined text-[20px] text-primary">zoom_out_map</span>
<span className="font-label-sm text-label-sm font-bold">View Map</span>
</a>
<a className="min-h-[52px] rounded-2xl bg-surface-container-low text-on-surface hover:bg-surface-container clay-card p-2 flex flex-col items-center justify-center gap-0.5 text-center active:scale-95 transition-all" data-path="live-hazard-map" href="#">
<span className="material-symbols-outlined text-[20px] text-tertiary">alt_route</span>
<span className="font-label-sm text-label-sm font-bold">Safe Route</span>
</a>
<a className="min-h-[52px] rounded-2xl bg-secondary-container text-on-secondary-container clay-pop p-2 flex flex-col items-center justify-center gap-0.5 text-center active:scale-95 transition-all" data-path="incident-reporter" href="#">
<span className="material-symbols-outlined text-[20px]">report</span>
<span className="font-label-sm text-label-sm font-bold">Report</span>
</a>
</div>
</section>
{/*  NEARBY INCIDENTS & LIVE ALERTS  */}
<section className="flex flex-col gap-space-sm">
<div className="flex items-center justify-between px-1">
<h3 className="font-title-md text-title-md text-on-surface font-bold tracking-tight">Nearby Incidents</h3>
<span className="font-label-sm text-label-sm text-on-surface-variant">2 within precinct</span>
</div>
{/*  Caution Incident Card 1  */}
<div className="rounded-3xl p-4 bg-surface-container-lowest clay-card flex items-center justify-between gap-space-md hover:bg-surface-container-low transition-colors">
<div className="flex items-center gap-3.5 min-w-0">
<div className="w-12 h-12 rounded-2xl bg-amber-100 text-amber-700 flex items-center justify-center shrink-0 clay-card">
<span className="material-symbols-outlined text-[24px]">tsunami</span>
</div>
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-2">
<h4 className="font-label-lg text-label-lg font-bold text-on-surface truncate">Flooding on 4th Ave</h4>
<span className="px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 font-label-sm text-label-sm font-bold">Caution</span>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant truncate mt-0.5">Water level 35cm • Avoid low underpasses</p>
</div>
</div>
<div className="flex flex-col items-end shrink-0 pl-1">
<span className="font-label-sm text-label-sm font-bold text-primary">1.2 km</span>
<span className="font-body-sm text-body-sm text-on-surface-variant/70">8m ago</span>
</div>
</div>
{/*  Road Block Incident Card 2  */}
<div className="rounded-3xl p-4 bg-surface-container-lowest clay-card flex items-center justify-between gap-space-md hover:bg-surface-container-low transition-colors">
<div className="flex items-center gap-3.5 min-w-0">
<div className="w-12 h-12 rounded-2xl bg-secondary-fixed text-on-secondary-fixed flex items-center justify-center shrink-0 clay-card">
<span className="material-symbols-outlined text-[24px]">traffic</span>
</div>
<div className="flex flex-col min-w-0">
<div className="flex items-center gap-2">
<h4 className="font-label-lg text-label-lg font-bold text-on-surface truncate">Road Blocked: Oak Bridge</h4>
<span className="px-2 py-0.5 rounded-full bg-secondary-fixed-dim text-on-secondary-fixed font-label-sm text-label-sm font-bold">Detour</span>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant truncate mt-0.5">Fallen utility limb cleared by 10:30 AM</p>
</div>
</div>
<div className="flex flex-col items-end shrink-0 pl-1">
<span className="font-label-sm text-label-sm font-bold text-primary">2.5 km</span>
<span className="font-body-sm text-body-sm text-on-surface-variant/70">22m ago</span>
</div>
</div>
{/*  Active Alerts Banner Link  */}
<a className="rounded-3xl p-4 bg-gradient-to-r from-primary-fixed to-primary-container text-on-primary-container clay-pop flex items-center justify-between gap-3 active:scale-[0.99] transition-transform" data-path="active-alerts" href="#">
<div className="flex items-center gap-3">
<div className="w-10 h-10 rounded-xl bg-on-primary/20 backdrop-blur-sm flex items-center justify-center text-on-primary">
<span className="material-symbols-outlined text-[22px]">notification_important</span>
</div>
<div className="flex flex-col">
<span className="font-label-lg text-label-lg font-bold text-on-primary">Check Active Alerts (3)</span>
<span className="font-body-sm text-body-sm text-on-primary-container">Severe rain advisory and emergency contacts</span>
</div>
</div>
<div className="w-8 h-8 rounded-full bg-on-primary/10 flex items-center justify-center text-on-primary">
<span className="material-symbols-outlined text-[20px]">arrow_forward</span>
</div>
</a>
</section>
{/*  EMERGENCY PREPAREDNESS / COMMUNITY DELIGHT CARD  */}
<section className="rounded-3xl p-5 bg-surface-container-low clay-card flex flex-col gap-3 relative overflow-hidden">
<div className="flex items-center justify-between">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-primary text-[22px]">family_restroom</span>
<h4 className="font-title-md text-title-md font-bold text-on-surface">Family Check-in</h4>
</div>
<span className="font-label-sm text-label-sm text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full font-bold">All 3 Safe</span>
</div>
<div className="flex items-center justify-between pt-1">
<div className="flex items-center -space-x-2">
<img className="w-9 h-9 rounded-full object-cover ring-2 ring-surface clay-card"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCARUHMDhcnqhVqeresGApKU53oyUEE2FrGs7JFHzJ1RaNjcPVtjQf8aywsHCnJ4-AgNnri5brrHRkVQQ2dUMKXiMko8ikIOU2u7thGrbxe-3f6QuisbejA4FCLcIY5BxpEt6J7aZtScqdfd9B7tM0Q5xkJK8mXW5rfQgJGLX99hljESXDKJ2JRO9aL3ddl-O2PnjTgp_y27_8Z9VUkx3MGYqHnumyR9cwX3wYcwkrYrpvpUYC1IPzlCQ" />
<img className="w-9 h-9 rounded-full object-cover ring-2 ring-surface clay-card"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCgjjHyAG-scn5Z9D1vT08F9-BuZkEN4ZUT_nqJgVwAavP7133NEkJ9qY3ddJnEyNnOt412sANjnagngn2E0DAPFIm-Qt4cSMoEpKFDKtmwyxxFn1X4frGQcQynf-zzCdh7fus_6psnKbUnXKYEsbK_MC9CX8QVIEiw5lN-8EueW70tSIVlHljlzgAU01N4PCdxgQd3MBE6srXSXAMdjOQFTfTdcm641NLq1fTH4SWz1IBJO_B5onGvAQ" />
<img className="w-9 h-9 rounded-full object-cover ring-2 ring-surface clay-card"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuAEiVtlkSnSmH4GkB1LLLY2uZ8D5IUFm5FndUEA1vqQyqZeCv7hH4s74q1evcz5Ja-HbdE2Zuo-PfgkUCGJmAQtt4bozzs1WyfM9rZEFRMrI7wv8l32HPyP0lM5zvJrk08i0SOQCxcfcLHZAsFqD4FP11xXJyImDq3MZ0uv2mlfa01R6ETsDgq6f-GsJSraiWgcBZ3fWrKvo23AyTQKPhhGgFCSJnmNSMRSjRNKmaaAdBZSkBxBUNp3qA" />
</div>
<button className="px-3.5 py-1.5 rounded-full bg-surface-container-lowest text-primary font-label-md text-label-md font-bold clay-card hover:bg-surface transition-all active:scale-95" id="pingCircleBtn" type="button">
        Ping Circle
      </button>
</div>
</section>
</div></>
  );
}

export default CitizenDashboard;
