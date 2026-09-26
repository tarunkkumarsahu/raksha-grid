import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Splash from './pages/Splash';
import Login from './pages/Login';
import CitizenDashboard from './pages/CitizenDashboard';
import ReportIncident from './pages/ReportIncident';
import ResponseTeamDashboard from './pages/ResponseTeamDashboard';
import ResponseTeamIncidentDetails from './pages/ResponseTeamIncidentDetails';
import ResponseTeamMap from './pages/ResponseTeamMap';
import SafeRoute from './pages/SafeRoute';
import CitizenAlerts from './pages/CitizenAlerts';
import CitizenMap from './pages/CitizenMap';
import ResponseTeamIncidents from './pages/ResponseTeamIncidents';
import RegistrationScreen from './pages/RegistrationScreen';

function NavMenu() {
  return (
    <div className="fixed top-0 left-0 z-50 p-2 bg-black/80 text-white text-xs flex gap-2 flex-wrap">
      <a href="/" className="underline">Splash</a>
      <a href="/login" className="underline">Login</a>
      <a href="/citizendashboard" className="underline">CitizenDashboard</a>
      <a href="/reportincident" className="underline">ReportIncident</a>
      <a href="/responseteamdashboard" className="underline">ResponseTeamDashboard</a>
      <a href="/responseteamincidentdetails" className="underline">ResponseTeamIncidentDetails</a>
      <a href="/responseteammap" className="underline">ResponseTeamMap</a>
      <a href="/saferoute" className="underline">SafeRoute</a>
      <a href="/citizenalerts" className="underline">CitizenAlerts</a>
      <a href="/citizenmap" className="underline">CitizenMap</a>
      <a href="/responseteamincidents" className="underline">ResponseTeamIncidents</a>
      <a href="/register" className="underline">RegistrationScreen</a>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <NavMenu />
      <Routes>
        <Route path="/" element={<Splash />} />
        <Route path="/login" element={<Login />} />
        <Route path="/citizendashboard" element={<CitizenDashboard />} />
        <Route path="/reportincident" element={<ReportIncident />} />
        <Route path="/responseteamdashboard" element={<ResponseTeamDashboard />} />
        <Route path="/responseteamincidentdetails" element={<ResponseTeamIncidentDetails />} />
        <Route path="/responseteammap" element={<ResponseTeamMap />} />
        <Route path="/saferoute" element={<SafeRoute />} />
        <Route path="/citizenalerts" element={<CitizenAlerts />} />
        <Route path="/citizenmap" element={<CitizenMap />} />
        <Route path="/responseteamincidents" element={<ResponseTeamIncidents />} />
        <Route path="/register" element={<RegistrationScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
