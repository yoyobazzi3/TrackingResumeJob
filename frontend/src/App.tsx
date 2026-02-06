import { useState } from "react";
import { AuthProvider, useAuth } from "./auth/AuthContext";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";

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
      <Dashboard />
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
