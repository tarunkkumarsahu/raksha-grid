import { Link } from 'react-router-dom';

function ResponseTeamIncidentDetails() {
  return (
    <><div className="flex flex-col w-full pb-safe pb-2">
{/*  Subtle Ambient Atmospheric Glow Blobs behind Clay Containers  */}
<div className="relative w-full px-margin pt-space-md space-y-space-lg overflow-hidden">
<div className="absolute -top-12 -right-16 w-64 h-64 bg-primary-fixed-dim/20 rounded-full blur-3xl pointer-events-none -z-10"></div>
<div className="absolute top-1/3 -left-20 w-72 h-72 bg-tertiary-fixed-dim/15 rounded-full blur-3xl pointer-events-none -z-10"></div>
<div className="absolute bottom-20 right-0 w-80 h-80 bg-secondary-fixed/30 rounded-full blur-3xl pointer-events-none -z-10"></div>
{/*  1. Incident Summary Card  */}
<section className="w-full bg-surface-container-lowest rounded-xl p-space-lg shadow-[10px_16px_24px_-4px_rgba(51,47,58,0.08),4px_6px_10px_-2px_rgba(124,58,237,0.04)] relative">
<div className="flex items-center justify-between gap-space-sm mb-space-md">
{/*  Severity Badge (Pill with inner specular highlight)  */}
<div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-error-container text-on-error-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.7),inset_-2px_-2px_4px_rgba(147,0,10,0.12)]">
<span className="material-symbols-outlined text-[16px] animate-pulse" >emergency</span>
<span className="font-label-sm text-label-sm uppercase tracking-wider">HIGH PRIORITY</span>
</div>
{/*  Mesh Network Bead Indicator  */}
<div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_3px_6px_rgba(51,47,58,0.04)]">
<span className="w-2 h-2 rounded-full bg-tertiary shadow-[0_0_6px_rgba(0,84,121,0.6)] animate-ping"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-bold">LIVE MESH</span>
</div>
</div>
{/*  Incident Title  */}
<h2 className="font-headline-sm text-headline-sm text-on-surface mb-space-xs tracking-tight">
        Flash Flood: Riverfront &amp; 4th Ave
      </h2>
{/*  Reported metadata  */}
<div className="space-y-1.5 mb-space-md">
<div className="flex items-center gap-1.5 text-on-surface-variant">
<span className="material-symbols-outlined text-[18px] text-primary">verified_user</span>
<p className="font-body-md text-body-md">
            Reported by <span className="font-semibold text-on-surface">Citizen (Sarah Jenkins, Verified Resident)</span>
</p>
</div>
<div className="flex items-start gap-1.5 text-on-surface-variant">
<span className="material-symbols-outlined text-[18px] text-tertiary shrink-0 mt-0.5">near_me</span>
<p className="font-body-sm text-body-sm leading-snug">
            Sector 4 Downtown Precinct • GPS 47.6062° N, 122.3321° W
          </p>
</div>
<div className="flex items-center gap-1.5 text-outline">
<span className="material-symbols-outlined text-[16px]">schedule</span>
<p className="font-body-sm text-body-sm">
            Reported: 14 mins ago (09:27 AM) • <span className="text-secondary font-medium">Last Update: 3 mins ago</span>
</p>
</div>
</div>
{/*  Description Inset Clay Groove  */}
<div className="w-full bg-surface-container rounded-lg p-space-md mb-space-md shadow-[inset_2px_3px_5px_rgba(51,47,58,0.08),inset_-2px_-2px_4px_rgba(255,255,255,0.85)]">
<div className="flex items-center gap-1.5 text-primary mb-1">
<span className="material-symbols-outlined text-[16px]">chat_bubble_outline</span>
<span className="font-label-sm text-label-sm text-primary uppercase">Citizen Report</span>
</div>
<p className="font-body-md text-body-md text-on-surface leading-relaxed">
          “Storm drain overflowed, water level rapidly rising above curb (approx 45cm). Two vehicles stranded near overpass. Power lines buzzing.”
        </p>
</div>
{/*  Attached Evidence Thumbnail with Modal Preview  */}
<div className="flex items-center justify-between p-2 rounded-lg bg-surface-container-high shadow-[2px_3px_8px_rgba(51,47,58,0.06),inset_1px_1px_2px_rgba(255,255,255,0.8)]">
<div className="flex items-center gap-space-sm min-w-0">
<img className="w-14 h-14 rounded-DEFAULT object-cover shadow-[inset_1px_1px_2px_rgba(255,255,255,0.4)] shrink-0"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuDEUrMiYkvOsXIO10JgONqgMvdAAPC3w9MiGECUCvZa4NrQGZ5x_bjDwe6ePFU2L9KjuuFR-r3bwmebkqufa7ibmTjuN4o9x-JcBqAU11Nxte0PEr6gWCITmy0FYf-SwOx2NH0HphrXDboTtPwsWCIxGLE-t9RXWW7KeaSHJIg3fQcPAdChQq6OqW57lBlisOeG7e7P_MSfJzcTjHLAF9Ipj2tzQSZI-fPXOf61VA9KG5wKKHQw0_ZaZQ" />
<div className="min-w-0">
<p className="font-title-md text-body-md text-on-surface truncate font-semibold">Flood_curb_img.jpg</p>
<p className="font-body-sm text-body-sm text-on-surface-variant">Evidence • 2.4 MB • Geo-stamped</p>
</div>
</div>
<button aria-label="Expand image evidence" className="w-11 h-11 rounded-full bg-surface-container-lowest text-primary flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_4px_8px_rgba(51,47,58,0.1)] active:scale-95 transition-transform" id="evidence-preview-btn">
<span className="material-symbols-outlined text-[20px]">zoom_in</span>
</button>
</div>
</section>
{/*  2. Tactical Vector Map Card  */}
<section className="w-full bg-surface-container-lowest rounded-xl p-space-lg shadow-[10px_16px_24px_-4px_rgba(51,47,58,0.08),4px_6px_10px_-2px_rgba(124,58,237,0.04)] relative">
<div className="flex items-center justify-between mb-space-sm">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-primary text-[22px]">radar</span>
<h3 className="font-headline-sm text-headline-sm text-on-surface">Tactical Perimeter</h3>
</div>
<span className="font-label-sm text-label-sm px-2.5 py-1 rounded-full bg-tertiary-fixed text-on-tertiary-fixed font-bold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
          150m HAZARD RADIUS
        </span>
</div>
{/*  Recessed Tactical Vector Map Canvas  */}
<div className="relative w-full h-56 rounded-lg overflow-hidden mb-space-md bg-surface-container shadow-[inset_3px_4px_8px_rgba(51,47,58,0.12),inset_-2px_-2px_5px_rgba(255,255,255,0.9)]">
{/*  Stylized Vector Map Graphic  */}
<svg className="w-full h-full" fill="none" viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg">
{/*  Street Grids & Blocks  */}
<rect fill="#EDE5F4" height="220" width="320"></rect>
{/*  Urban blocks  */}
<rect fill="#F9F1FF" height="50" rx="8" width="70" x="20" y="20"></rect>
<rect fill="#F9F1FF" height="50" rx="8" width="90" x="110" y="20"></rect>
<rect fill="#F9F1FF" height="50" rx="8" width="80" x="220" y="20"></rect>
<rect fill="#F9F1FF" height="60" rx="8" width="70" x="20" y="90"></rect>
<rect fill="#F9F1FF" height="60" rx="8" width="80" x="220" y="90"></rect>
<rect fill="#F9F1FF" height="35" rx="8" width="130" x="20" y="170"></rect>
<rect fill="#F9F1FF" height="35" rx="8" width="130" x="170" y="170"></rect>
{/*  River/Waterfront Path  */}
<path d="M-10 115 C 80 110, 100 135, 330 118" opacity="0.6" stroke="#89CEFF" stroke-linecap="round" stroke-width="26"></path>
{/*  Flooded Danger Perimeter (Expanding clay ripple)  */}
<circle cx="160" cy="115" fill="#BA1A1A" fill-opacity="0.12" r="54" stroke="#BA1A1A" stroke-dasharray="4 4" stroke-width="2">
<animate attributeName="r" dur="3s" repeatCount="indefinite" values="50;58;50"></animate>
</circle>
<circle cx="160" cy="115" fill="#BA1A1A" fill-opacity="0.22" r="28"></circle>
{/*  Incident Epicenter Beacon  */}
<circle cx="160" cy="115" fill="#BA1A1A" r="9">
<animate attributeName="r" dur="1.4s" repeatCount="indefinite" values="8;12;8"></animate>
</circle>
<circle cx="160" cy="115" fill="#FFFFFF" r="4"></circle>
{/*  Street Names  */}
<text fill="#4A4455" font-family="DM Sans" font-size="9" font-weight="600" x="115" y="85">4TH AVE</text>
<text fill="#4A4455" font-family="DM Sans" font-size="8" font-weight="600" x="175" y="152">RIVERFRONT BLVD</text>
{/*  Accessible route lines  */}
<path d="M 60 190 L 60 140 L 120 140" stroke="#7C3AED" stroke-dasharray="2 6" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"></path>
{/*  Responder Current Position Bead (Alpha-4)  */}
<circle cx="60" cy="190" fill="#7C3AED" r="11"></circle>
<circle cx="60" cy="190" fill="#EDE0FF" r="5"></circle>
<text fill="#630ED4" font-family="Nunito Sans" font-size="10" font-weight="800" x="78" y="194">Alpha-4 (YOU)</text>
{/*  Staged Mutual Aid Unit (Squad 2)  */}
<circle cx="270" cy="45" fill="#005479" r="8"></circle>
<circle cx="270" cy="45" fill="#CFE9FF" r="3.5"></circle>
<text fill="#005479" font-family="Nunito Sans" font-size="9" font-weight="700" x="225" y="40">Squad 2</text>
</svg>
{/*  Compass Rose Clay Float  */}
<div className="absolute top-2 right-2 w-8 h-8 rounded-full bg-surface-container-lowest/90 backdrop-blur-sm shadow-[1px_2px_4px_rgba(51,47,58,0.15)] flex items-center justify-center text-primary font-label-sm font-bold">
          N
        </div>
</div>
{/*  Action Buttons on Map Card  */}
<div className="flex flex-col sm:flex-row gap-space-sm"><button id="open-operational-map-btn" className="flex-1 py-3.5 px-space-md rounded-DEFAULT bg-gradient-to-r from-primary-container to-primary text-on-primary font-headline-sm text-title-md flex items-center justify-center gap-2 shadow-[0px_14px_24px_-6px_rgba(124,58,237,0.38),inset_2px_2px_4px_rgba(255,255,255,0.45),inset_-3px_-3px_6px_rgba(0,0,0,0.15)] active:scale-95 transition-all"><span className="">OPEN OPERATIONAL MAP</span><span className="text-[18px]">🗺️</span></button><button id="start-response-route-btn" className="flex-1 py-3.5 px-space-md rounded-DEFAULT bg-surface-container text-on-surface font-headline-sm text-title-md flex items-center justify-center gap-2 shadow-[inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.06),3px_5px_12px_rgba(51,47,58,0.08)] active:scale-95 transition-all"><span className="">START RESPONSE ROUTE</span><span className="text-[18px]">🧭</span></button></div>
</section>
{/*  3. Response Status Section (CRITICAL WORKFLOW)  */}
<section className="w-full bg-surface-container-lowest rounded-xl p-space-lg shadow-[10px_16px_24px_-4px_rgba(51,47,58,0.08),4px_6px_10px_-2px_rgba(124,58,237,0.04)]">
<div className="flex items-center gap-2 mb-space-xs">
<span className="material-symbols-outlined text-secondary text-[22px]">swap_horizontal_circle</span>
<h3 className="font-headline-sm text-headline-sm text-on-surface">Update Operational Status</h3>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant mb-space-md">
        Select unit stage and submit confirmation to SafePath Central Dispatch.
      </p>
{/*  4-State Clay Selector Buttons Grid  */}
<div className="grid grid-cols-2 gap-space-sm mb-space-md" id="status-button-group">
{/*  State 1: NEW  */}
<button className="status-btn py-3 px-space-sm rounded-DEFAULT text-center font-headline-sm text-title-md bg-surface-container text-on-surface-variant shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_3px_6px_rgba(51,47,58,0.06)] active:scale-95 transition-all" data-status="NEW" type="button">
          NEW
        </button>
{/*  State 2: ACKNOWLEDGED (Active selected state with amber clay highlight & checkmark)  */}
<button className="status-btn py-3 px-space-sm rounded-DEFAULT text-center font-headline-sm text-title-md bg-gradient-to-br from-amber-300 via-amber-400 to-amber-500 text-on-surface shadow-[0px_10px_20px_-4px_rgba(217,119,6,0.4),inset_2px_2px_4px_rgba(255,255,255,0.65),inset_-2px_-2px_4px_rgba(0,0,0,0.12)] active:scale-95 transition-all flex items-center justify-center gap-1.5 ring-0" data-status="ACKNOWLEDGED" type="button">
<span className="material-symbols-outlined text-[20px]" >check_circle</span>
<span className="">ACKNOWLEDGED</span>
</button>
{/*  State 3: IN PROGRESS  */}
<button className="status-btn py-3 px-space-sm rounded-DEFAULT text-center font-headline-sm text-title-md bg-surface-container text-on-surface-variant shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_3px_6px_rgba(51,47,58,0.06)] active:scale-95 transition-all" data-status="IN PROGRESS" type="button">
          IN PROGRESS
        </button>
{/*  State 4: RESOLVED  */}
<button className="status-btn py-3 px-space-sm rounded-DEFAULT text-center font-headline-sm text-title-md bg-surface-container text-on-surface-variant shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_3px_6px_rgba(51,47,58,0.06)] active:scale-95 transition-all" data-status="RESOLVED" type="button">
          RESOLVED
        </button>
</div>
{/*  Status Notes Recessed Clay Groove Input  */}
<div className="mb-space-md">
<label className="block font-label-md text-label-md text-on-surface font-semibold mb-1.5" htmlFor="status-note">
          Dispatch Log Transmission
        </label>
<div className="relative w-full rounded-DEFAULT bg-surface-container shadow-[inset_3px_3px_6px_rgba(51,47,58,0.1),inset_-2px_-2px_4px_rgba(255,255,255,0.9)] p-1">
<textarea className="w-full bg-transparent p-space-sm font-body-md text-body-md text-on-surface placeholder:text-outline focus:outline-none resize-none" id="status-note" placeholder="Optional dispatch note..." rows="2"></textarea>
</div>
</div>
{/*  Primary Raised Clay Button: UPDATE STATUS  */}
<button className="w-full py-4 px-space-lg rounded-DEFAULT bg-gradient-to-r from-primary-container to-primary text-on-primary font-headline-sm text-title-md tracking-wide shadow-[0px_14px_28px_-6px_rgba(124,58,237,0.38),inset_2px_2px_4px_rgba(255,255,255,0.45),inset_-3px_-3px_6px_rgba(0,0,0,0.15)] active:scale-[0.98] transition-all flex items-center justify-center gap-2" id="update-status-submit-btn">
<span className="material-symbols-outlined text-[20px]">send</span>
<span className="">UPDATE STATUS</span>
</button>
{/*  Active feedback indicator  */}
<div className="mt-space-sm flex items-center justify-center gap-2 py-2 px-space-md rounded-full bg-surface-container text-tertiary shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_2px_5px_rgba(51,47,58,0.04)]" id="status-feedback">
<span className="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
<span className="font-label-md text-label-md font-semibold tracking-tight">Status: Acknowledged by Unit Alpha-4</span>
</div>
</section>
{/*  4. Deployed Units & Mutual Aid  */}
<section className="w-full bg-surface-container-lowest rounded-xl p-space-lg shadow-[10px_16px_24px_-4px_rgba(51,47,58,0.08),4px_6px_10px_-2px_rgba(124,58,237,0.04)] mb-space-lg">
<div className="flex items-center justify-between mb-space-md">
<div className="flex items-center gap-2">
<span className="material-symbols-outlined text-primary text-[22px]">local_police</span>
<h3 className="font-headline-sm text-headline-sm text-on-surface">Units &amp; Mutual Aid</h3>
</div>
<span className="font-label-sm text-label-sm px-2.5 py-1 rounded-full bg-surface-container text-on-surface-variant font-bold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9)]">
          2 ACTIVE
        </span>
</div>
<div className="space-y-space-sm">
{/*  Unit 1: Alpha-4  */}
<div className="p-space-md rounded-lg bg-surface-container-low flex items-center justify-between shadow-[3px_5px_10px_rgba(51,47,58,0.04),inset_1px_1px_2px_rgba(255,255,255,0.9)]">
<div className="flex items-center gap-space-sm">
<div className="w-10 h-10 rounded-full bg-primary-container text-on-primary flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.45),2px_4px_8px_rgba(124,58,237,0.25)]">
<span className="material-symbols-outlined text-[20px]">directions_car</span>
</div>
<div>
<div className="flex items-center gap-1.5">
<p className="font-title-md text-title-md text-on-surface font-bold">Alpha-4</p>
<span className="font-label-sm text-label-sm px-1.5 py-0.5 rounded bg-primary-fixed text-on-primary-fixed font-bold">YOUR UNIT</span>
</div>
<p className="font-body-sm text-body-sm text-on-surface-variant">En route • ETA 4 min</p>
</div>
</div>
<button aria-label="Radio Alpha-4" className="w-10 h-10 rounded-full bg-surface-container text-primary flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_3px_6px_rgba(51,47,58,0.08)] active:scale-95 transition-transform">
<span className="material-symbols-outlined text-[18px]">radio</span>
</button>
</div>
{/*  Unit 2: Rescue Squad 2  */}
<div className="p-space-md rounded-lg bg-surface-container-low flex items-center justify-between shadow-[3px_5px_10px_rgba(51,47,58,0.04),inset_1px_1px_2px_rgba(255,255,255,0.9)]">
<div className="flex items-center gap-space-sm">
<div className="w-10 h-10 rounded-full bg-tertiary text-on-tertiary flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.45),2px_4px_8px_rgba(0,84,121,0.25)]">
<span className="material-symbols-outlined text-[20px]">support</span>
</div>
<div>
<p className="font-title-md text-title-md text-on-surface font-bold">Rescue Squad 2</p>
<p className="font-body-sm text-body-sm text-on-surface-variant">Staged at 2nd Ave • Standby water rescue</p>
</div>
</div>
<button aria-label="Radio Squad 2" className="w-10 h-10 rounded-full bg-surface-container text-tertiary flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),2px_3px_6px_rgba(51,47,58,0.08)] active:scale-95 transition-transform">
<span className="material-symbols-outlined text-[18px]">phone_in_talk</span>
</button>
</div>
</div>
</section>
</div>
{/*  Interactive Evidence Lightbox Modal (Hidden by Default)  */}
<div className="fixed inset-0 z-50 bg-inverse-surface/60 backdrop-blur-md hidden items-center justify-center p-margin" id="evidence-modal">
<div className="w-full max-w-sm bg-surface-container-lowest rounded-xl p-space-md shadow-2xl relative">
<div className="flex items-center justify-between pb-2 mb-2">
<h4 className="font-headline-sm text-title-md text-on-surface">Flood_curb_img.jpg</h4>
<button className="w-8 h-8 rounded-full bg-surface-container text-on-surface flex items-center justify-center shadow-sm" id="evidence-modal-close">
<span className="material-symbols-outlined text-[18px]">close</span>
</button>
</div>
<img className="w-full h-64 rounded-DEFAULT object-cover mb-space-sm"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCwijbSXbKhTBTPYH7cnZ_Xpk4rDzb5MkCdORDj8pONoLwkmY69Wzml48j_dHdGm31J-IsLBrTiO_kqa9ETzd28AtoL2SP3mdvwxRWRsrPTC5URx_w2totavDZ7Q2kg68THB4VGFc0PsCWbFTQBURIpCjOfeVODIx80_K3Cs6230jXctk2xJYUj6C8OeBE4K3zBQeVkfBu1h2MetIt4mYtalvLDiPPRjTVk0QL1qkUx4ZI9L_Z1TFxFhA" />
<p className="font-body-sm text-body-sm text-on-surface-variant">
        Attached by citizen Sarah Jenkins. Certified tamper-evident hash #SHA-8924.
      </p>
</div>
</div><div className="fixed inset-0 z-50 bg-inverse-surface/60 backdrop-blur-md hidden items-center justify-center p-margin" id="route-nav-modal"><div className="w-full max-w-sm bg-surface-container-lowest rounded-xl p-space-lg shadow-2xl relative"><div className="flex items-center justify-between pb-2 mb-space-sm"><div className="flex items-center gap-2"><span className="material-symbols-outlined text-primary text-[22px]">navigation</span><h4 className="font-headline-sm text-title-md text-on-surface">Active Tactical Route</h4></div><button className="w-8 h-8 rounded-full bg-surface-container text-on-surface flex items-center justify-center shadow-sm" id="route-modal-close"><span className="material-symbols-outlined text-[18px]">close</span></button></div><div className="p-space-md rounded-lg bg-surface-container mb-space-md shadow-[inset_2px_2px_4px_rgba(51,47,58,0.06)]"><p className="font-body-md font-semibold text-primary mb-1">Target: Riverfront &amp; 4th Ave</p><p className="font-body-sm text-on-surface-variant leading-relaxed">Alpha-4 routing via 3rd Ave Overpass. ETA 4 mins. Hazard perimeter alert active.</p></div><button className="w-full py-3.5 px-space-md rounded-DEFAULT bg-gradient-to-r from-primary-container to-primary text-on-primary font-headline-sm text-title-md shadow-[0px_14px_24px_-6px_rgba(124,58,237,0.38)] active:scale-95 transition-all text-center" id="route-nav-confirm">PROCEED ON ROUTE</button></div></div><div className="fixed inset-0 z-50 bg-inverse-surface/60 backdrop-blur-md hidden items-center justify-center p-margin" id="profile-modal"><div className="w-full max-w-sm bg-surface-container-lowest rounded-xl p-space-lg shadow-2xl relative"><div className="flex items-center justify-between pb-2 mb-space-sm"><h4 className="font-headline-sm text-title-md text-on-surface">Response Unit Profile</h4><button className="w-8 h-8 rounded-full bg-surface-container text-on-surface flex items-center justify-center shadow-sm" id="profile-modal-close"><span className="material-symbols-outlined text-[18px]">close</span></button></div><div className="flex items-center gap-space-sm mb-space-md"><img alt="Responder Officer" className="w-14 h-14 rounded-full object-cover shadow-[inset_1px_1px_2px_rgba(255,255,255,0.4)]" src="https://lh3.googleusercontent.com/aida/AEtjO1U7FPGYB6sFQts5Cd1LCFng6t1OoDgcGloBBJiHKsZ-34UqEPZhwP9g_2Tz0QO60LHUv5UkksFQPCbh4eZuz4eV4DRyu2nFCI_GQ1xguCU8faFo-ZsRlTkVXjbnq9IZWYEeYBDsEL_JbnH6XozmeoN4PAb5mMYMEbKnXj0Y5-0v4a4mZKAsZTIcGickj-txoeCZxVons2hOXlwMXOeRr4AGioGTLDYckFQR1F4zarbfaIFlxV0OJHJ2Sco" /><div><p className="font-title-md font-bold text-on-surface">Officer J. Vance</p><p className="font-body-sm text-on-surface-variant">Alpha-4 Rapid Response Team</p><span className="font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-tertiary-fixed text-on-tertiary-fixed font-bold mt-1 inline-flex">STATION 4</span></div></div><div className="p-space-sm bg-surface-container rounded-lg mb-space-md"><p className="font-body-sm text-on-surface-variant">Duty Status: <span className="font-bold text-secondary">ON SCENE ASSIGNED</span></p></div><button className="w-full py-3 px-space-md rounded-DEFAULT bg-surface-container text-on-surface font-headline-sm text-body-md text-center active:scale-95 transition-all shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9)]" id="profile-modal-dismiss">Close Profile</button></div></div>
</div></>
  );
}

export default ResponseTeamIncidentDetails;
