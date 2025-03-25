import "./App.css";
import Login from "./components/Login";
import { useEffect, useState } from "react";

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
        <h1>Minha Aplicação</h1>

        <Login />

        <div>
          <h2>Dados do Backend:</h2>
          <pre>{data ? JSON.stringify(data, null, 2) : "Carregando..."}</pre>
        </div>
      </header>
    </div>
  );
}

export default App;
