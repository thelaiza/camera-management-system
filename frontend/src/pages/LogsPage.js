import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/LogsPage.css";
import { useNavigate } from "react-router-dom";

function LogsPage() {
  const [logs, setLogs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const carregarLogs = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/logs/");
        setLogs(res.data.logs);
      } catch (error) {
        console.error("Erro ao carregar logs:", error);
      }
    };
    carregarLogs();
  }, []);

  return (
    <div className="logs-container">
      <header className="logs-header">
        <button className="back-button" onClick={() => navigate("/home")}>←</button>
        <img src="/logo.png" alt="Logo" className="logo" />
      </header>

      <h2 className="logs-title">Logs</h2>

      <table className="logs-table">
        <thead>
          <tr>
            <th>Ação</th>
            <th>Usuário</th>
            <th>Câmera</th>
            <th>Data e hora da ação</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{log.acao}</td>
              <td>{log.usuario_id || "-"}</td>
              <td>{log.camera_id || "-"}</td>
              <td>{new Date(log.data_hora).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default LogsPage;
