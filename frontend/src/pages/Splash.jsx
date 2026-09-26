import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Splash() {
  const [progress, setProgress] = useState('w-0');
  const [btnScale, setBtnScale] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const timer1 = setTimeout(() => {
      setProgress('w-[85%]');
    }, 400);

    const timer2 = setTimeout(() => {
      setProgress('w-full');
    }, 1200);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);

  const handleContinue = () => {
    setBtnScale('scale-[0.96]');
    setTimeout(() => {
      setBtnScale('');
      navigate('/login'); // Redirect to login page!
    }, 150);
  };

  return (
    <main className="flex-1 flex flex-col relative w-full pt-safe pb-safe px-margin bg-surface min-h-screen">
      <div className="flex flex-col w-full relative overflow-hidden py-space-xl items-center justify-between min-h-[82vh]">
        
        {/* Atmospheric Clay Ambient Orbs */}
        <div className="absolute -top-24 -left-20 w-72 h-72 rounded-full bg-primary-fixed blur-3xl opacity-40 pointer-events-none"></div>
        <div className="absolute top-1/3 -right-24 w-80 h-80 rounded-full bg-secondary-fixed blur-3xl opacity-35 pointer-events-none"></div>
        <div className="absolute -bottom-16 left-1/4 w-64 h-64 rounded-full bg-tertiary-fixed blur-3xl opacity-30 pointer-events-none"></div>
        
        {/* Top Connectivity & Readiness Status Pill */}
        <div className="relative z-10 w-full flex justify-center pt-space-sm">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-surface-container-lowest shadow-[0_8px_18px_-4px_rgba(51,47,58,0.06),inset_2px_2px_4px_rgba(255,255,255,0.9),inset_-2px_-2px_4px_rgba(51,47,58,0.04)]">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-container opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary-container"></span>
            </span>
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Mesh Node Ready</span>
            <span className="material-symbols-outlined text-sm text-primary-container leading-none">satellite_alt</span>
          </div>
        </div>
        
        {/* Main Center Claymorphic Emblem & Branding Group */}
        <div className="relative z-10 flex flex-col items-center text-center my-auto px-margin max-w-sm w-full">
          <div className="relative group cursor-pointer mb-space-lg transition-transform duration-300 active:scale-95">
            <div className="absolute -inset-4 rounded-3xl bg-gradient-to-tr from-primary-fixed via-primary-container/20 to-secondary-fixed blur-xl opacity-60 group-hover:opacity-80 transition-opacity"></div>
            <div className="relative w-36 h-36 rounded-3xl bg-gradient-to-br from-primary-fixed-dim via-primary-container to-primary flex items-center justify-center p-3 shadow-[12px_22px_32px_-6px_rgba(99,14,212,0.32),inset_3px_3px_6px_0px_rgba(255,255,255,0.65),inset_-4px_-4px_8px_0px_rgba(0,0,0,0.2)]">
              <div className="w-full h-full rounded-2xl flex items-center justify-center overflow-hidden bg-gradient-to-br from-primary-container/30 to-primary/80 shadow-[inset_2px_2px_4px_rgba(255,255,255,0.4)]">
                <img alt="SafePath Emblem" className="w-28 h-28 object-contain drop-shadow-[0_8px_16px_rgba(37,0,90,0.25)] select-none pointer-events-none" src="https://lh3.googleusercontent.com/aida/AEtjO1X5BR96gcIkpu5gIXDqp7bXNUxnVhNDWB8keWvzXrtX9jMPaUnVsZIIHvIFE3iWOLhRdyj8bCR9VtMveetGSFOtjmfAoFTRbC7VKBtR78lKn1bTD6_mSYiuki-U_UomdQcgqPv9vZx2Jt4gmIUAwlXzxuUGp4aIQEkskwBf2DQwruNaZ8K3M4K6AYbyQeOIOYx_7_aoCbRKVXJKrAgGpDRvI2hKzGxQOgG-HkGd2qeecXVck14E_WPyxVk"/>
              </div>
            </div>
          </div>
          
          <div className="mb-space-sm">
            <span className="inline-flex items-center px-3.5 py-1 rounded-full bg-surface-container-high text-primary font-label-sm text-label-sm tracking-widest uppercase shadow-[inset_1px_1px_3px_rgba(51,47,58,0.06),inset_-1px_-1px_3px_rgba(255,255,255,0.8)]">
              Disaster Response
            </span>
          </div>
          
          <h1 className="font-display-lg-mobile text-display-lg-mobile text-inverse-surface tracking-tight mb-space-xs">
            SafePath
          </h1>
          
          <p className="font-body-md text-body-md text-on-surface-variant max-w-[260px] leading-relaxed">
            Safer communities, calmer minds, stronger together.
          </p>
          
          <div className="w-44 h-2.5 rounded-full bg-surface-container-highest mt-space-lg p-0.5 shadow-[inset_2px_2px_4px_rgba(51,47,58,0.14),inset_-1px_-1px_2px_rgba(255,255,255,0.9)] overflow-hidden">
            <div className={`h-full rounded-full bg-gradient-to-r from-primary via-primary-container to-secondary-container transition-all duration-700 ease-out shadow-[0_2px_4px_rgba(124,58,237,0.35)] ${progress}`} id="splash-progress-bar"></div>
          </div>
        </div>
        
        <div className="relative z-10 w-full max-w-sm flex flex-col items-center gap-space-sm px-margin pb-space-sm">
          <button 
            className={`w-full flex items-center justify-center gap-2 py-4 px-6 rounded-2xl bg-gradient-to-br from-primary-container to-primary text-on-primary font-label-lg text-label-lg shadow-[0px_14px_28px_-6px_rgba(124,58,237,0.38),inset_2px_2px_4px_0px_rgba(255,255,255,0.45),inset_-3px_-3px_6px_0px_rgba(0,0,0,0.18)] transition-all duration-150 ${btnScale}`} 
            type="button"
            onClick={handleContinue}
          >
            <span>Get Started</span>
            <span className="material-symbols-outlined text-lg leading-none">arrow_forward</span>
          </button>
          
          <div className="flex items-center justify-between w-full pt-space-xs px-2">
            <div className="flex items-center gap-1.5 text-on-surface-variant">
              <span className="material-symbols-outlined text-base text-primary">verified_user</span>
              <span className="font-body-sm text-body-sm">Offline First Ready</span>
            </div>
            <button className="font-label-sm text-label-sm text-primary hover:text-primary-container transition-colors py-1 px-2 rounded-lg focus:outline-none" type="button">
              Regional Notice
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

export default Splash;
