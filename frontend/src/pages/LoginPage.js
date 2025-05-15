import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/Login.css";
import logo from "../assets/logo.png";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/api/login/", {
        email: email,
        senha: senha,
      });
  
      // Salvando no LocalStorage
      localStorage.setItem("user_id", res.data.id);
      localStorage.setItem("usuario_nome", res.data.nome);
      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);
  
      navigate("/home");
    } catch (err) {
      console.error("Erro no login:", err.response?.data || err.message);
      setErro("Login inválido. Tente novamente.");
    }
  };
  
  return (
    <div className="login-page">
      <div className="login-card">
        <img src={logo} alt="Logo" className="login-logo" />
        {erro && <p style={{ color: "red" }}>{erro}</p>}
        <input
          className="login-input"
          type="text"
          placeholder="Login"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="login-input"
          type="password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
        />
        <button className="login-button" onClick={handleLogin}>
          Entrar
        </button>
      </div>
    </div>
  );
}

export default LoginPage;
