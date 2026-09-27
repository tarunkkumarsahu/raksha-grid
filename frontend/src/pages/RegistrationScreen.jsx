import { Link } from 'react-router-dom';

function RegistrationScreen() {
  return (
    <><div className="flex flex-col w-full relative pb-8">
<div className="absolute -top-12 -left-14 w-56 h-56 rounded-full bg-primary-fixed/40 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute top-72 -right-16 w-60 h-60 rounded-full bg-secondary-fixed/30 blur-3xl pointer-events-none -z-10"></div>
<div className="absolute bottom-20 left-6 w-48 h-48 rounded-full bg-tertiary-fixed/30 blur-3xl pointer-events-none -z-10"></div>
<div className="flex items-center justify-between mt-2 mb-4">
<button aria-label="Return to Login" className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full bg-surface-container text-on-surface hover:text-primary transition-all active:scale-95 clay-card"  type="button">
<span className="material-symbols-outlined text-[20px]">arrow_back</span>
</button>
<div className="inline-flex items-center gap-1.5 py-1 px-3.5 rounded-full bg-surface-container-high/80 backdrop-blur-sm shadow-sm">
<span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
<span className="font-label-sm text-label-sm text-on-surface-variant font-bold tracking-wide uppercase">Mesh Node Ready</span>
</div>
</div>
<div className="flex flex-col items-center text-center mb-6">
<div className="relative mb-3 flex items-center justify-center">
<div className="w-16 h-16 rounded-[22px] bg-gradient-to-tr from-primary to-primary-container flex items-center justify-center clay-pop relative z-10">
<span className="material-symbols-outlined text-[32px] text-on-primary" >verified_user</span>
</div>
<div className="absolute inset-0 bg-primary-container/20 rounded-[22px] blur-md scale-110"></div>
</div>
<h2 className="font-headline-md text-headline-md text-on-surface font-extrabold tracking-tight">Create Your Account</h2>
<p className="font-body-md text-body-md text-on-surface-variant mt-1 max-w-xs">
      Join SafePath to stay connected, secure loved ones, and coordinate critical response.
    </p>
</div>
<form className="flex flex-col gap-4" id="registrationForm" >
<div className="flex flex-col gap-1.5">
<label className="font-label-md text-label-md text-on-surface font-semibold pl-1 flex items-center gap-1.5" htmlFor="fullName">
<span className="material-symbols-outlined text-[16px] text-primary">person</span> Full Name
      </label>
<div className="relative flex items-center">
<input className="w-full h-13 py-3 pl-4 pr-11 rounded-[20px] bg-surface-container-highest/60 text-on-surface font-body-md text-body-md placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary-container/40 transition-all" id="fullName" placeholder="Enter your full name" required=""  type="text"/>
<span className="material-symbols-outlined absolute right-3.5 text-outline text-[18px] pointer-events-none">badge</span>
</div>
</div>
<div className="flex flex-col gap-1.5">
<label className="font-label-md text-label-md text-on-surface font-semibold pl-1 flex items-center gap-1.5" htmlFor="email">
<span className="material-symbols-outlined text-[16px] text-primary">mail</span> Email Address
      </label>
<div className="relative flex items-center">
<input className="w-full h-13 py-3 pl-4 pr-11 rounded-[20px] bg-surface-container-highest/60 text-on-surface font-body-md text-body-md placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary-container/40 transition-all" id="email" placeholder="Enter your email" required=""  type="email"/>
<span className="material-symbols-outlined absolute right-3.5 text-outline text-[18px] pointer-events-none">alternate_email</span>
</div>
</div>
<div className="flex flex-col gap-1.5">
<label className="font-label-md text-label-md text-on-surface font-semibold pl-1 flex items-center gap-1.5" htmlFor="password">
<span className="material-symbols-outlined text-[16px] text-primary">lock</span> Create Password
      </label>
<div className="relative flex items-center">
<input className="w-full h-13 py-3 pl-4 pr-11 rounded-[20px] bg-surface-container-highest/60 text-on-surface font-body-md text-body-md placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary-container/40 transition-all" id="password" placeholder="Create password" required=""  type="password"/>
<button className="absolute right-2.5 min-w-[36px] min-h-[36px] flex items-center justify-center text-outline hover:text-on-surface transition-colors"  type="button">
<span className="material-symbols-outlined text-[18px]">visibility</span>
</button>
</div>
</div>
<div className="flex flex-col gap-1.5">
<label className="font-label-md text-label-md text-on-surface font-semibold pl-1 flex items-center gap-1.5" htmlFor="confirmPassword">
<span className="material-symbols-outlined text-[16px] text-primary">lock_reset</span> Confirm Password
      </label>
<div className="relative flex items-center">
<input className="w-full h-13 py-3 pl-4 pr-11 rounded-[20px] bg-surface-container-highest/60 text-on-surface font-body-md text-body-md placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary-container/40 transition-all" id="confirmPassword" placeholder="Confirm password" required=""  type="password"/>
<button className="absolute right-2.5 min-w-[36px] min-h-[36px] flex items-center justify-center text-outline hover:text-on-surface transition-colors"  type="button">
<span className="material-symbols-outlined text-[18px]">visibility</span>
</button>
</div>
</div>
<div className="flex flex-col gap-2.5 mt-2">
<div className="flex items-center justify-between px-1">
<span className="font-title-md text-title-md text-on-surface font-bold">I am a...</span>
<span className="font-label-sm text-label-sm text-primary font-bold tracking-wider uppercase">Select Role</span>
</div>
<div aria-label="Account role selection" className="grid grid-cols-2 gap-3" role="radiogroup">
<div aria-checked="true" className="cursor-pointer flex flex-col justify-between p-3.5 rounded-[24px] bg-surface-container-lowest transition-all duration-200 clay-pop relative overflow-hidden select-none" id="roleCitizen"  role="radio" tabindex="0">
<div className="flex items-start justify-between">
<div className="w-10 h-10 rounded-[14px] bg-primary-fixed flex items-center justify-center text-primary transition-colors" id="citizenIconWrapper">
<span className="material-symbols-outlined text-[22px]" >shield</span>
</div>
<div className="w-6 h-6 rounded-full bg-primary-container text-on-primary flex items-center justify-center shadow-sm" id="citizenBadge">
<span className="material-symbols-outlined text-[14px] font-bold">check</span>
</div>
</div>
<div className="mt-4">
<h3 className="font-headline-sm text-headline-sm text-primary font-black tracking-tight leading-tight" id="citizenTitle">CITIZEN</h3>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5 leading-snug">Personal safety &amp; local alerts</p>
</div>
</div>
<div aria-checked="false" className="cursor-pointer flex flex-col justify-between p-3.5 rounded-[24px] bg-surface-container opacity-85 transition-all duration-200 clay-card relative overflow-hidden select-none hover:opacity-100" id="roleResponder"  role="radio" tabindex="0">
<div className="flex items-start justify-between">
<div className="w-10 h-10 rounded-[14px] bg-surface-container-high flex items-center justify-center text-on-surface-variant transition-colors" id="responderIconWrapper">
<span className="material-symbols-outlined text-[22px]">medical_services</span>
</div>
<div className="w-6 h-6 rounded-full bg-surface-container-highest text-transparent flex items-center justify-center transition-all" id="responderBadge">
<span className="material-symbols-outlined text-[14px]">check</span>
</div>
</div>
<div className="mt-4">
<h3 className="font-headline-sm text-headline-sm text-on-surface font-black tracking-tight leading-tight" id="responderTitle">RESPONSE TEAM</h3>
<p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5 leading-snug">Incident response &amp; coordination</p>
</div>
</div>
</div>
</div>
<div className="p-3 rounded-[20px] bg-surface-container-lowest/80 clay-card flex items-center gap-3 mt-1">
<div className="w-9 h-9 rounded-full bg-secondary-fixed/50 flex items-center justify-center text-secondary shrink-0">
<span className="material-symbols-outlined text-[18px]">cell_tower</span>
</div>
<div className="min-w-0 flex-1">
<div className="font-label-md text-label-md text-on-surface font-bold leading-tight">Offline Mesh Fallback</div>
<div className="font-body-sm text-body-sm text-on-surface-variant truncate">Auto-sync when cell towers go dark</div>
</div>
</div>
<button className="mt-3 w-full py-4 rounded-[20px] text-on-primary font-headline-sm text-headline-sm font-extrabold tracking-wide text-center transition-all active:scale-[0.98] clay-pop flex items-center justify-center gap-2" id="submitBtn"  type="submit">
<span>CREATE ACCOUNT</span>
<span className="material-symbols-outlined text-[22px]">arrow_forward</span>
</button>
</form>
<div className="flex items-center justify-center mt-6">
<button className="py-2.5 px-4 rounded-full bg-surface-container text-on-surface hover:text-primary transition-all active:scale-95 clay-card flex items-center gap-1.5"  type="button">
<span className="font-body-md text-body-md text-on-surface-variant">Already have an account?</span>
<span className="font-label-md text-label-md text-primary font-bold underline decoration-primary/40 underline-offset-4">LOGIN</span>
</button>
</div>
<div className="fixed bottom-4 left-margin right-margin bg-inverse-surface text-inverse-on-surface p-4 rounded-[22px] shadow-2xl transition-all duration-300 transform translate-y-36 opacity-0 flex items-center justify-between z-50" id="routeBanner">
<div className="flex items-center gap-3">
<div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-on-primary shrink-0">
<span className="material-symbols-outlined text-[18px]">verified</span>
</div>
<div className="flex flex-col">
<span className="font-label-md text-label-md font-bold" id="routeBannerTitle">Account Created!</span>
<span className="font-body-sm text-body-sm opacity-80" id="routeBannerSub">Routing to Citizen SafeZone...</span>
</div>
</div>
<span className="material-symbols-outlined animate-spin text-primary-fixed">autorenew</span>
</div>
</div></>
  );
}

export default RegistrationScreen;
