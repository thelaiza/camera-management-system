import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";
import logo from "../assets/logo.png";

function Login() {
  const navigate = useNavigate();

  return (
    <div className="login-page">
      <div className="login-card">
        <img src={logo} alt="Logo" className="login-logo" />
        <input className="login-input" type="text" placeholder="Login" />
        <input className="login-input" type="password" placeholder="Senha" />
        <button className="login-button" onClick={() => navigate("/home")}>
          Entrar
        </button>
      </div>
    </div>
  );
}

export default Login;
