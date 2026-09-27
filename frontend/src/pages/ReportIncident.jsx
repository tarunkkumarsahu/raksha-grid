import { Link } from 'react-router-dom';

function ReportIncident() {
  return (
    <><div className="flex flex-col w-full relative">
{/*  Ambient Soft Blobs for Claymorphic Glow  */}
<div className="absolute -top-12 -left-10 w-48 h-48 rounded-full bg-primary/10 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute top-80 -right-12 w-56 h-56 rounded-full bg-secondary/10 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute bottom-20 left-4 w-60 h-60 rounded-full bg-tertiary-fixed/40 blur-3xl pointer-events-none -z-10"></div>
{/*  Navigation / Context Bar  */}
<div className="flex items-center justify-between py-space-sm mb-space-md">
<a className="flex items-center gap-space-xs px-3.5 py-2 rounded-full bg-surface-container clay-card active:scale-95 transition-all text-on-surface-variant hover:text-primary" data-path="home-citizen-dashboard" href="#">
<span className="material-symbols-outlined text-[18px]">arrow_back</span>
<span className="font-label-md text-label-md font-bold">Dashboard</span>
</a>
<div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-low clay-card">
<span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-medium">SafePath Live Mesh</span>
</div>
</div>
{/*  Intro Narrative Block  */}
<div className="mb-space-lg">
<div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed mb-space-xs clay-card">
<span className="material-symbols-outlined text-[16px]" >add_alert</span>
<span className="font-label-sm text-label-sm font-bold uppercase tracking-wider">Citizen Dispatch</span>
</div>
<h2 className="font-headline-lg text-headline-lg text-inverse-surface tracking-tight mb-1">
      Report an Incident
    </h2>
<p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
      Help response teams understand what is happening. Your report updates live maps and directs nearby mutual aid.
    </p>
</div>
{/*  Form Area Container  */}
<form className="flex flex-col gap-space-lg pb-safe" id="incidentForm" >
{/*  1. INCIDENT TYPE SELECTOR  */}
<section className="flex flex-col gap-space-sm">
<div className="flex items-center justify-between">
<label className="font-title-md text-title-md text-inverse-surface font-bold flex items-center gap-2">
<span>1. What happened?</span>
<span className="text-secondary font-bold text-sm">*</span>
</label>
<span className="font-label-sm text-label-sm text-primary font-semibold" id="selectedCategoryBadge">Flood Selected</span>
</div>
<div className="grid grid-cols-2 sm:grid-cols-3 gap-3" id="incidentTypeGroup">
{/*  Flood (Active Default)  */}
<button className="incident-chip flex flex-col items-center justify-center p-4 rounded-2xl text-center transition-all bg-primary-container text-on-primary-container clay-pop ring-2 ring-primary" data-type="Flood" type="button">
<div className="w-12 h-12 rounded-full flex items-center justify-center bg-white/20 mb-2">
<span className="material-symbols-outlined text-[28px]" >tsunami</span>
</div>
<span className="font-label-lg text-label-lg font-bold">Flood</span>
<span className="font-body-sm text-body-sm opacity-90 mt-0.5">Rising waters</span>
</button>
{/*  Fire  */}
<button className="incident-chip flex flex-col items-center justify-center p-4 rounded-2xl text-center transition-all bg-surface-container text-on-surface clay-card hover:bg-surface-container-high" data-type="Fire" type="button">
<div className="w-12 h-12 rounded-full flex items-center justify-center bg-secondary-fixed text-on-secondary-fixed mb-2">
<span className="material-symbols-outlined text-[28px]">local_fire_department</span>
</div>
<span className="font-label-lg text-label-lg font-bold">Fire</span>
<span className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Smoke / Blaze</span>
</button>
{/*  Road Blocked  */}
<button className="incident-chip flex flex-col items-center justify-center p-4 rounded-2xl text-center transition-all bg-surface-container text-on-surface clay-card hover:bg-surface-container-high" data-type="Road Blocked" type="button">
<div className="w-12 h-12 rounded-full flex items-center justify-center bg-surface-container-highest text-on-surface-variant mb-2">
<span className="material-symbols-outlined text-[28px]">traffic_jam</span>
</div>
<span className="font-label-lg text-label-lg font-bold">Blocked Way</span>
<span className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Debris or tree</span>
</button>
{/*  Building Damage  */}
<button className="incident-chip flex flex-col items-center justify-center p-4 rounded-2xl text-center transition-all bg-surface-container text-on-surface clay-card hover:bg-surface-container-high" data-type="Building Damage" type="button">
<div className="w-12 h-12 rounded-full flex items-center justify-center bg-tertiary-fixed text-on-tertiary-fixed mb-2">
<span className="material-symbols-outlined text-[28px]">home_work</span>
</div>
<span className="font-label-lg text-label-lg font-bold">Structural</span>
<span className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Collapse / Glass</span>
</button>
{/*  Medical  */}
<button className="incident-chip flex flex-col items-center justify-center p-4 rounded-2xl text-center transition-all bg-surface-container text-on-surface clay-card hover:bg-surface-container-high" data-type="Medical Emergency" type="button">
<div className="w-12 h-12 rounded-full flex items-center justify-center bg-error-container text-on-error-container mb-2">
<span className="material-symbols-outlined text-[28px]">medical_services</span>
</div>
<span className="font-label-lg text-label-lg font-bold">Medical</span>
<span className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Injured citizen</span>
</button>
{/*  Other  */}
<button className="incident-chip flex flex-col items-center justify-center p-4 rounded-2xl text-center transition-all bg-surface-container text-on-surface clay-card hover:bg-surface-container-high" data-type="Other" type="button">
<div className="w-12 h-12 rounded-full flex items-center justify-center bg-surface-variant text-on-surface-variant mb-2">
<span className="material-symbols-outlined text-[28px]">emergency</span>
</div>
<span className="font-label-lg text-label-lg font-bold">Other</span>
<span className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Utility / Power</span>
</button>
</div>
</section>
{/*  2. LOCATION SECTION  */}
<section className="flex flex-col gap-space-sm">
<label className="font-title-md text-title-md text-inverse-surface font-bold flex items-center justify-between">
<span>2. Where is it?</span>
<span className="font-label-sm text-label-sm text-emerald-700 font-semibold flex items-center gap-1">
<span className="material-symbols-outlined text-[14px]">lock</span> High Accuracy GPS
        </span>
</label>
{/*  Primary GPS Auto-detect Button  */}
<button className="flex items-center justify-between p-4 rounded-2xl bg-surface-container text-on-surface clay-card hover:bg-surface-container-high active:scale-[0.99] transition-all text-left" id="gpsAutoBtn" type="button">
<div className="flex items-center gap-3">
<div className="w-11 h-11 rounded-full flex items-center justify-center bg-primary text-on-primary shadow-md">
<span className="material-symbols-outlined text-[22px]">my_location</span>
</div>
<div className="flex flex-col">
<span className="font-label-lg text-label-lg font-bold text-on-surface">Use current location</span>
<span className="font-body-sm text-body-sm text-on-surface-variant font-mono">GPS: 47.6062° N, 122.3321° W (Pine &amp; 4th)</span>
</div>
</div>
<div className="w-7 h-7 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-700">
<span className="material-symbols-outlined text-[18px]" >check_circle</span>
</div>
</button>
{/*  Map Selector Link/Button  */}
<button className="flex items-center justify-center gap-2 py-3 px-4 rounded-2xl bg-surface-container-low text-primary font-label-md text-label-md font-bold clay-card hover:bg-surface-container transition-all" type="button">
<span className="material-symbols-outlined text-[20px]">explore</span>
<span>Pinpoint on interactive map</span>
</button>
{/*  Interactive Micro-Map Preview Snippet  */}
<div className="relative w-full h-24 rounded-2xl overflow-hidden clay-card mt-1">
<div className="w-full h-full bg-cover bg-center" data-location="Pine Street &amp; 4th Avenue, Seattle" ></div>
<div className="absolute inset-0 bg-primary/10 backdrop-blur-[1px] flex items-center justify-center pointer-events-none">
<div className="px-3 py-1.5 rounded-full bg-surface/95 text-inverse-surface font-label-sm text-label-sm font-bold flex items-center gap-1.5 shadow-md">
<span className="w-2.5 h-2.5 rounded-full bg-secondary animate-ping"></span>
            Pin active: 140m from your spot
          </div>
</div>
</div>
</section>
{/*  3. DESCRIPTION SECTION  */}
<section className="flex flex-col gap-space-sm">
<div className="flex items-center justify-between">
<label className="font-title-md text-title-md text-inverse-surface font-bold" htmlFor="incidentNotes">
          3. Tell us what happened
        </label>
<span className="font-label-sm text-label-sm text-on-surface-variant" id="charCounter">0/280</span>
</div>
<div className="relative rounded-2xl bg-[#EAE5F5] p-1 shadow-[inset_3px_4px_8px_0px_rgba(51,47,58,0.12),inset_-2px_-2px_5px_0px_rgba(255,255,255,0.9)] focus-within:ring-2 focus-within:ring-primary/40 transition-all">
<textarea className="w-full bg-transparent border-0 outline-none p-3 font-body-md text-body-md text-on-surface placeholder:text-outline-variant resize-none" id="incidentNotes" maxlength="280" placeholder="Describe the situation briefly (e.g., storm drain overflowed, knee-deep water advancing toward retail shops, power lines buzzing)..." rows="3"></textarea>
</div>
{/*  Quick-Add Pill Prompts  */}
<div className="flex items-center gap-2 overflow-x-auto py-1 no-scrollbar text-on-surface-variant">
<span className="font-label-sm text-label-sm text-outline shrink-0">Quick tag:</span>
<button className="quick-pill shrink-0 px-3 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm clay-card active:scale-95 transition-transform" data-text="Rapidly rising water." type="button">
          + Rising fast
        </button>
<button className="quick-pill shrink-0 px-3 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm clay-card active:scale-95 transition-transform" data-text="Road impassable for standard vehicles." type="button">
          + Road impassable
        </button>
<button className="quick-pill shrink-0 px-3 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm clay-card active:scale-95 transition-transform" data-text="Need sandbags immediately." type="button">
          + Sandbags needed
        </button>
</div>
</section>
{/*  4. SEVERITY SELECTOR  */}
<section className="flex flex-col gap-space-sm">
<div className="flex items-center justify-between">
<label className="font-title-md text-title-md text-inverse-surface font-bold">
          4. How serious is it?
        </label>
<span className="font-label-sm text-label-sm text-secondary font-bold uppercase" id="severityDisplay">Medium Hazard</span>
</div>
<div className="grid grid-cols-3 gap-2.5" id="severityGroup">
{/*  Low  */}
<button className="severity-card flex flex-col items-center p-3 rounded-2xl text-center bg-surface-container text-on-surface clay-card transition-all" data-severity="Low" type="button">
<div className="w-9 h-9 rounded-full flex items-center justify-center bg-emerald-100 text-emerald-800 mb-1.5">
<span className="material-symbols-outlined text-[20px]">eco</span>
</div>
<span className="font-label-md text-label-md font-bold text-on-surface">Low</span>
<span className="font-body-sm text-body-sm text-on-surface-variant scale-90">Minor issue</span>
</button>
{/*  Medium (Selected Default)  */}
<button className="severity-card flex flex-col items-center p-3 rounded-2xl text-center bg-amber-500 text-white clay-pop ring-2 ring-amber-400 transition-all" data-severity="Medium" type="button">
<div className="w-9 h-9 rounded-full flex items-center justify-center bg-white/20 text-white mb-1.5">
<span className="material-symbols-outlined text-[20px]" >warning</span>
</div>
<span className="font-label-md text-label-md font-bold">Medium</span>
<span className="font-body-sm text-body-sm text-amber-50 scale-90">Needs caution</span>
</button>
{/*  High  */}
<button className="severity-card flex flex-col items-center p-3 rounded-2xl text-center bg-surface-container text-on-surface clay-card transition-all" data-severity="High" type="button">
<div className="w-9 h-9 rounded-full flex items-center justify-center bg-secondary-fixed text-on-secondary-fixed mb-1.5">
<span className="material-symbols-outlined text-[20px]">e911_emergency</span>
</div>
<span className="font-label-md text-label-md font-bold text-on-surface">High</span>
<span className="font-body-sm text-body-sm text-on-surface-variant scale-90">Urgent danger</span>
</button>
</div>
</section>
{/*  5. MEDIA ATTACHMENT  */}
<section className="flex flex-col gap-space-sm">
<label className="font-title-md text-title-md text-inverse-surface font-bold">
        5. Visual Evidence
      </label>
<div className="grid grid-cols-2 gap-3">
{/*  Add Photo Trigger  */}
<button className="flex flex-col items-center justify-center p-5 rounded-2xl bg-surface-container-low text-primary clay-card hover:bg-surface-container active:scale-95 transition-all text-center" id="addMediaBtn" type="button">
<div className="w-12 h-12 rounded-full bg-primary-fixed flex items-center justify-center text-on-primary-fixed mb-1 shadow-inner">
<span className="material-symbols-outlined text-[24px]">add_a_photo</span>
</div>
<span className="font-label-md text-label-md font-bold mt-1">+ Photo / Video</span>
<span className="font-body-sm text-body-sm text-on-surface-variant">(Optional proof)</span>
</button>
{/*  Verified Thumbnail Preview (Demonstrating Media Attachment)  */}
<div className="relative rounded-2xl overflow-hidden clay-card h-28 group">
<img className="w-full h-full object-cover"  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCzXAqzF6ET-6bRvjSn3nSI5ec7ltM4GauKFjcpowgiIfFcm-qtosnJagAvE2MzyRDEh-lxkUrICQDAAY3oA5cnsRPwEqwzNt_90Q3n7ZzQS3j37Sy2i2S2axnFAUa9Xql8Cr3e7p4QUuPBg56bJbTb0BjgHFr4O8ztd0wnKtAEBLsSfUbGOki1dwezuY-DaWpfe9miu3AddR9s8qsOQCIYl8PQViIuU0r9xH7CREzUrAcbf2dyQSAHMA"/>
<div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-2 justify-between">
<span className="text-white font-label-sm text-label-sm font-semibold truncate">IMG_0842.jpg</span>
<button className="w-6 h-6 rounded-full bg-surface text-secondary flex items-center justify-center active:scale-90 shadow" type="button">
<span className="material-symbols-outlined text-[14px]">close</span>
</button>
</div>
</div>
</div>
</section>
{/*  SUBMISSION AREA  */}
<div className="mt-space-md flex flex-col gap-space-sm">
{/*  Primary Clay CTA Button  */}
<button className="w-full min-h-[56px] py-3.5 px-6 rounded-2xl text-on-primary font-headline-sm text-headline-sm font-bold flex items-center justify-center gap-2 bg-gradient-to-r from-[#A78BFA] to-[#7C3AED] clay-pop active:scale-[0.98] transition-transform" id="submitBtn" type="submit">
<span className="material-symbols-outlined text-[24px]" >send</span>
<span>SUBMIT REPORT</span>
</button>
<p className="font-body-sm text-body-sm text-on-surface-variant text-center px-4 leading-normal">
        Your report will be shared immediately with the local response coordination team and peer citizens in this sector.
      </p>
</div>
</form>
{/*  POPUP / SUCCESS MODAL (Hidden by default, triggered on submit)  */}
<div className="hidden fixed inset-0 z-50 flex items-center justify-center p-space-md bg-inverse-surface/40 backdrop-blur-md" id="successModal">
<div className="w-full max-w-sm rounded-3xl bg-surface p-space-lg clay-card flex flex-col items-center text-center animate-[bounce_0.4s_ease-out]">
{/*  Success Badge Graphic  */}
<div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-primary-fixed to-primary text-on-primary flex items-center justify-center clay-pop mb-space-md">
<span className="material-symbols-outlined text-[44px]" >verified_user</span>
</div>
<div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 font-label-sm text-label-sm font-bold mb-2">
<span className="material-symbols-outlined text-[14px]">sensors</span> Dispatch Received #SF-8921
      </div>
<h3 className="font-headline-md text-headline-md text-inverse-surface font-bold tracking-tight mb-2">
        Report Transmitted!
      </h3>
<p className="font-body-md text-body-md text-on-surface-variant mb-space-lg leading-relaxed">
        Thank you for keeping your community safe. Responders in District 4 have received your GPS coordinates and incident notes.
      </p>
<div className="w-full flex flex-col gap-2">
<a className="w-full py-3.5 px-4 rounded-2xl bg-primary text-on-primary font-label-lg text-label-lg font-bold clay-pop text-center" data-path="live-hazard-map" href="#">
          View on Live Map
        </a>
<a className="w-full py-3 px-4 rounded-2xl bg-surface-container text-on-surface font-label-md text-label-md font-bold clay-card text-center hover:bg-surface-container-high" data-path="home-citizen-dashboard" href="#">
          Return to Dashboard
        </a>
</div>
</div>
</div>
</div></>
  );
}

export default ReportIncident;
