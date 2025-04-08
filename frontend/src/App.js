import "./App.css";
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";
import CamerasPage from "./pages/CamerasPage";
import UsuariosPage from "./pages/UsuariosPage";
import LogsPage from "./pages/LogsPage";


function App() {
  const [data, setData] = useState(null);

  // Requisição ao backend Django
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/") 
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error("Erro ao buscar dados:", error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <Router>
        <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/cameras" element={<CamerasPage />} />
        <Route path="/usuarios" element={<UsuariosPage />} />
        <Route path="/logs" element={<LogsPage />} />
      </Routes>
    </Router>
      </header>
    </div>
  );
}


export default App;
