import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";
import CamerasPage from "./pages/CamerasPage";
import UsuariosPage from "./pages/UsuariosPage";
import LogsPage from "./pages/LogsPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/cameras" element={<CamerasPage />} />
        <Route path="/usuarios" element={<UsuariosPage />} />
        <Route path="/logs" element={<LogsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
