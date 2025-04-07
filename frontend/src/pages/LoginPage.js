import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

function LoginPage() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // simula login com sucesso
    navigate("/home");
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
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

export default LoginPage;
