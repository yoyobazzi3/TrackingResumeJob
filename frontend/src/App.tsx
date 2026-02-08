import { useState } from "react";
import { AuthProvider, useAuth } from "./auth/AuthContext";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import JobApplicationsPage from "./pages/JobApplicationsPage";
import { Routes, Route, NavLink } from "react-router-dom";

function AppContent() {
  const { token, logout } = useAuth();
  const [mode, setMode] = useState<"login" | "signup">("login");

  if (!token) {
    return (
      <div className="auth-shell">
        {mode === "login" ? (
          <Login onSwitch={() => setMode("signup")} />
        ) : (
          <Signup onSwitch={() => setMode("login")} />
        )}
      </div>
    );
  }

  return (
    <div>
      <nav className="app-nav">
        <div className="app-nav__inner">
          <div className="app-nav__brand">Resume Hub</div>
          <div className="app-nav__links">
            <NavLink to="/" end>
              Dashboard
            </NavLink>
            <NavLink to="/applications">Applications</NavLink>
          </div>
          <button className="secondary" onClick={logout}>
            Logout
          </button>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/applications" element={<JobApplicationsPage />} />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
