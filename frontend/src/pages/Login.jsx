import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [showPassword, setShowPassword] = useState(false);
  const [showError, setShowError] = useState(false);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [email, setEmail] = useState('clara.oswald@safepath.org');
  const [password, setPassword] = useState('password123');
  const navigate = useNavigate();

  const handlePrimaryLogin = (e) => {
    e.preventDefault();
    if (!email) {
      setShowError(true);
      return;
    }
    
    setIsAuthenticating(true);
    setTimeout(() => {
      setIsAuthenticating(false);
      // In a real app we'd navigate to citizen-dashboard, but let's just alert for now or route.
      alert("Logged in! Imagine navigating to the dashboard now.");
    }, 800);
  };

  return (
    <main className="flex-1 flex flex-col relative w-full pt-safe pb-safe px-margin bg-surface min-h-screen">
      <div className="flex flex-col w-full max-w-md mx-auto relative pb-8 pt-10">
        
        <div className="absolute -top-12 -left-12 w-64 h-64 rounded-full bg-primary-fixed-dim/30 blur-3xl pointer-events-none -z-10"></div>
        <div className="absolute top-48 -right-16 w-56 h-56 rounded-full bg-secondary-fixed/40 blur-3xl pointer-events-none -z-10"></div>
        <div className="absolute bottom-10 left-8 w-48 h-48 rounded-full bg-tertiary-fixed/30 blur-3xl pointer-events-none -z-10"></div>
        
        <div className="flex flex-col items-center justify-center pt-4 pb-6">
          <div className="relative flex items-center justify-center w-24 h-24 rounded-3xl bg-gradient-to-br from-surface-container-lowest to-surface-container-low shadow-[10px_16px_28px_-6px_rgba(51,47,58,0.12),4px_6px_12px_-2px_rgba(124,58,237,0.06)] [box-shadow:10px_16px_24px_-4px_rgba(51,47,58,0.1),_inset_3px_3px_6px_0px_rgba(255,255,255,0.9),_inset_-4px_-4px_8px_0px_rgba(51,47,58,0.05)] p-4 transition-transform active:scale-95 duration-200">
            <img alt="SafePath Shield Icon" className="w-full h-full object-contain filter drop-shadow-sm select-none pointer-events-none" src="https://lh3.googleusercontent.com/aida/AEtjO1X5BR96gcIkpu5gIXDqp7bXNUxnVhNDWB8keWvzXrtX9jMPaUnVsZIIHvIFE3iWOLhRdyj8bCR9VtMveetGSFOtjmfAoFTRbC7VKBtR78lKn1bTD6_mSYiuki-U_UomdQcgqPv9vZx2Jt4gmIUAwlXzxuUGp4aIQEkskwBf2DQwruNaZ8K3M4K6AYbyQeOIOYx_7_aoCbRKVXJKrAgGpDRvI2hKzGxQOgG-HkGd2qeecXVck14E_WPyxVk"/>
          </div>
          <div className="mt-4 flex items-center gap-1.5">
            <span className="font-headline-md text-headline-md text-inverse-surface tracking-tight">SafePath</span>
            <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-primary-fixed text-primary font-label-sm text-label-sm shadow-[inset_1px_1px_2px_rgba(255,255,255,0.7)]">v2.4</span>
          </div>
          <h1 className="mt-3 font-display-lg-mobile text-display-lg-mobile text-inverse-surface text-center">Welcome Back!</h1>
          <p className="mt-1 font-body-md text-body-md text-on-surface-variant text-center">Login to your SafePath account</p>
        </div>

        {showError && (
          <div className="mb-5 p-3.5 rounded-2xl bg-error-container text-on-error-container shadow-[inset_2px_2px_4px_rgba(147,0,10,0.15)] flex items-start gap-2.5 transition-all duration-300">
            <span className="material-symbols-outlined text-error text-[20px] shrink-0 mt-0.5" style={{fontVariationSettings: "'FILL' 1"}}>error</span>
            <div className="flex-1">
              <p className="font-title-md text-body-md font-bold text-on-error-container">Invalid Credentials</p>
              <p className="font-body-sm text-body-sm text-on-error-container/80 mt-0.5">Please check your email and password. If the mesh network is offline, peer verify instead.</p>
            </div>
            <button className="text-on-error-container hover:opacity-70 p-1" onClick={() => setShowError(false)} type="button">
              <span className="material-symbols-outlined text-[18px]">close</span>
            </button>
          </div>
        )}

        <form className="flex flex-col gap-4" onSubmit={handlePrimaryLogin}>
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-label-md text-inverse-surface pl-1" htmlFor="email">Email</label>
            <div className="relative flex items-center rounded-2xl bg-surface-container [box-shadow:inset_3px_4px_8px_0px_rgba(51,47,58,0.11),_inset_-2px_-2px_5px_0px_rgba(255,255,255,0.95)] px-4 py-3.5 transition-all focus-within:shadow-[inset_2px_2px_5px_rgba(51,47,58,0.08),0_0_0_2px_rgba(124,58,237,0.35)]">
              <span className="material-symbols-outlined text-outline text-[22px] shrink-0 mr-3">mail</span>
              <input 
                className="w-full bg-transparent font-body-md text-body-md text-inverse-surface placeholder:text-outline focus:outline-none" 
                id="email" 
                name="email" 
                placeholder="Enter your email" 
                required 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>
          
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-label-md text-inverse-surface pl-1" htmlFor="password">Password</label>
            <div className="relative flex items-center rounded-2xl bg-surface-container [box-shadow:inset_3px_4px_8px_0px_rgba(51,47,58,0.11),_inset_-2px_-2px_5px_0px_rgba(255,255,255,0.95)] px-4 py-3.5 transition-all focus-within:shadow-[inset_2px_2px_5px_rgba(51,47,58,0.08),0_0_0_2px_rgba(124,58,237,0.35)]">
              <span className="material-symbols-outlined text-outline text-[22px] shrink-0 mr-3">lock</span>
              <input 
                className="w-full bg-transparent font-body-md text-body-md text-inverse-surface placeholder:text-outline focus:outline-none" 
                id="password" 
                name="password" 
                placeholder="Enter your password" 
                required 
                type={showPassword ? "text" : "password"} 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button aria-label="Toggle password visibility" className="p-1 rounded-lg text-outline hover:text-primary transition-colors focus:outline-none shrink-0" onClick={() => setShowPassword(!showPassword)} type="button">
                <span className="material-symbols-outlined text-[20px]">{showPassword ? 'visibility_off' : 'visibility'}</span>
              </button>
            </div>
          </div>
          
          <div className="flex justify-end pr-1">
            <a className="font-label-md text-label-md text-primary-container font-semibold hover:underline" href="#forgot-password">Forgot password?</a>
          </div>
          
          <button 
            className="mt-2 w-full py-4 rounded-2xl bg-gradient-to-r from-primary-fixed-dim via-primary-container to-primary text-on-primary font-headline-sm text-headline-sm font-bold tracking-wide [box-shadow:0px_14px_26px_-6px_rgba(124,58,237,0.4),_inset_2px_2px_4px_0px_rgba(255,255,255,0.45),_inset_-3px_-3px_6px_0px_rgba(0,0,0,0.2)] active:scale-[0.98] transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-70" 
            type="submit"
            disabled={isAuthenticating}
          >
            {isAuthenticating ? (
              <>
                <span className="material-symbols-outlined animate-spin text-[20px]">sync</span>
                <span>AUTHENTICATING...</span>
              </>
            ) : (
              <>
                <span>LOGIN</span>
                <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
              </>
            )}
          </button>
        </form>

        <div className="my-6 flex items-center gap-3">
          <div className="h-0.5 flex-1 bg-surface-container-highest rounded-full"></div>
          <span className="font-label-sm text-label-sm text-outline uppercase tracking-wider">Quick Role Switch</span>
          <div className="h-0.5 flex-1 bg-surface-container-highest rounded-full"></div>
        </div>

        <div className="flex flex-col gap-2.5">
          <button className="w-full p-3.5 rounded-2xl bg-surface-container-lowest [box-shadow:6px_10px_20px_-4px_rgba(51,47,58,0.06),_inset_2px_2px_4px_0px_rgba(255,255,255,0.9),_inset_-2px_-2px_4px_0px_rgba(51,47,58,0.03)] flex items-center justify-between group active:scale-[0.99] transition-all" onClick={() => alert('Navigate to Citizen Dashboard')} type="button">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-tertiary-fixed flex items-center justify-center text-tertiary [box-shadow:inset_2px_2px_4px_rgba(255,255,255,0.8)]">
                <span className="material-symbols-outlined text-[20px]" style={{fontVariationSettings: "'FILL' 1"}}>person_pin_circle</span>
              </div>
              <div className="flex flex-col text-left">
                <span className="font-label-lg text-label-lg text-inverse-surface">Login as Citizen</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant">Citizen Safety Dashboard</span>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <span className="px-2.5 py-1 rounded-full bg-tertiary-container/15 text-tertiary-container font-label-sm text-label-sm font-bold">Citizen</span>
              <span className="material-symbols-outlined text-outline group-hover:translate-x-0.5 transition-transform text-[20px]">chevron_right</span>
            </div>
          </button>

          <button className="w-full p-3.5 rounded-2xl bg-surface-container-lowest [box-shadow:6px_10px_20px_-4px_rgba(51,47,58,0.06),_inset_2px_2px_4px_0px_rgba(255,255,255,0.9),_inset_-2px_-2px_4px_0px_rgba(51,47,58,0.03)] flex items-center justify-between group active:scale-[0.99] transition-all" onClick={() => alert('Navigate to Responder Dashboard')} type="button">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-secondary-fixed flex items-center justify-center text-secondary [box-shadow:inset_2px_2px_4px_rgba(255,255,255,0.8)]">
                <span className="material-symbols-outlined text-[20px]" style={{fontVariationSettings: "'FILL' 1"}}>medical_services</span>
              </div>
              <div className="flex flex-col text-left">
                <span className="font-label-lg text-label-lg text-inverse-surface">Login as Responder</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant">Response Team Ops Grid</span>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <span className="px-2.5 py-1 rounded-full bg-secondary-fixed text-on-secondary-fixed font-label-sm text-label-sm font-bold">Responder</span>
              <span className="material-symbols-outlined text-outline group-hover:translate-x-0.5 transition-transform text-[20px]">chevron_right</span>
            </div>
          </button>
        </div>

        <div className="mt-8 flex flex-col items-center justify-center gap-3">
          <p className="font-body-md text-body-md text-on-surface-variant text-center">
            Don't have an account? 
            <a className="font-headline-sm text-label-lg text-primary font-bold hover:underline tracking-tight ml-1" href="#register">REGISTER</a>
          </p>
          <button className="inline-flex items-center gap-1 py-1 px-3 rounded-full text-outline-variant hover:text-error hover:bg-error-container/20 transition-all font-label-sm text-label-sm" onClick={() => setShowError(true)} type="button">
            <span className="material-symbols-outlined text-[15px]">bug_report</span>
            <span>Simulate Login Error →</span>
          </button>
        </div>
        
        <div className="mt-6 flex items-center justify-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-[#10B981] shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
          <span className="font-body-sm text-body-sm text-outline">Offline Mesh Sync Ready • 256-bit Encrypted</span>
        </div>
      </div>
    </main>
  );
}

export default Login;
