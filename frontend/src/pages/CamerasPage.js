import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CamerasPage.css';
import { useNavigate } from "react-router-dom";

const CamerasPage = () => {
  const [cameras, setCameras] = useState([]);
  const [mostrarPopup, setMostrarPopup] = useState(false);
  const [nomeCamera, setNomeCamera] = useState("");
  const [localizacao, setLocalizacao] = useState("");
  const [status, setStatus] = useState("pendente");
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost:8000/api/cameras/')
      .then(response => setCameras(response.data))
      .catch(error => console.error('Erro ao buscar câmeras:', error));
  }, []);

  const handleAdicionarCamera = async () => {
    const usuario_id = localStorage.getItem("usuario_id");

    try {
      await axios.post("http://localhost:8000/api/cameras/adicionar/", {
        nome: nomeCamera,
        localizacao,
        status,
        usuario_id,
      });

      setNomeCamera("");
      setLocalizacao("");
      setStatus("pendente");
      setMostrarPopup(false);

      const res = await axios.get("http://localhost:8000/api/cameras/");
      setCameras(res.data);
    } catch (error) {
      console.error("Erro ao adicionar câmera:", error);
    }
  };

  return (
    <div className="cameras-container">
      <header className="cameras-header">
        <button className="back-button" onClick={() => navigate("/home")}>←</button>
        <img src="/logo.png" alt="Logo" className="logo" />
      </header>

      {mostrarPopup && (
        <div className="popup-overlay">
          <div className="popup-content popup-blue">
            <button className="popup-close" onClick={() => setMostrarPopup(false)}>X</button>
            <h3>Nova câmera</h3>
            <input
              type="text"
              placeholder="Nome"
              value={nomeCamera}
              onChange={(e) => setNomeCamera(e.target.value)}
              className="popup-input"
            />
            <input
              type="text"
              placeholder="Endereço"
              value={localizacao}
              onChange={(e) => setLocalizacao(e.target.value)}
              className="popup-input"
            />
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="popup-input"
            >
              <option value="pendente">Pendente</option>
              <option value="instalada">Instalada</option>
              <option value="removida">Removida</option>
            </select>
            <div className="popup-buttons">
              <button className="popup-confirm" onClick={handleAdicionarCamera}>Adicionar</button>
            </div>
          </div>
        </div>
      )}

      <div className="cameras-title-container">
        <h2 className="cameras-title">Câmeras</h2>
      </div>
      <div className="add-button-container">
        <button className="add-button" onClick={() => setMostrarPopup(true)}>Adicionar</button>
      </div>

      <div className="status-legend">
        <span><span className="dot green"></span>Instalada</span>
        <span><span className="dot red"></span>Removida</span>
        <span><span className="dot yellow"></span>Pendente</span>
      </div>

      <table className="camera-table">
        <thead>
          <tr>
            <th>Status</th>
            <th>ID</th>
            <th>Nome</th>
            <th>Endereço</th>
            <th>Usuário</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {cameras.map(camera => (
            <tr key={camera.id}>
              <td><span className={`dot ${camera.status}`}></span></td>
              <td>{camera.id}</td>
              <td>{camera.nome}</td>
              <td>{camera.localizacao}</td>
              <td>{camera.usuario || '-'}</td>
              <td className="actions">
                <span role="button" className="edit">✏️</span>
                <span role="button" className="delete">❌</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CamerasPage;
