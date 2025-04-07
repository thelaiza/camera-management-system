import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div>
      <h1>Bem-vindo ao CamIA Manager</h1>
      <nav>
        <ul>
          <li><Link to="/cameras">Gerenciar Câmeras</Link></li>
          <li><Link to="/usuarios">Gerenciar Usuários</Link></li>
          <li><Link to="/logs">Ver Logs</Link></li>
        </ul>
      </nav>
    </div>
  );
}

export default HomePage;
