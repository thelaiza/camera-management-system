import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Home.css";
import logo from "../assets/logo.png";

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <header className="home-header">
        <img src={logo} alt="Logo" className="logo" />
      </header>
      <main className="button-grid">
        <button onClick={() => navigate("/cameras")}>Câmeras</button>
        <button onClick={() => navigate("/usuarios")}>Usuários</button>
        <button onClick={() => navigate("/logs")}>Logs</button>
      </main>
    </div>
  );
}

export default HomePage;
