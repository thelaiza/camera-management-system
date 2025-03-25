import React from "react";
import "./Login.css"; 

function Login() {
  console.log("Login component renderizado!");
  return (
    <div className="login-container">
      <h2>Login</h2>
      <form>
        <div className="input-group">
          <label>Email:</label>
          <input type="email" placeholder="Digite seu email" required />
        </div>
        <div className="input-group">
          <label>Senha:</label>
          <input type="password" placeholder="Digite sua senha" required />
        </div>
        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}

export default Login;
