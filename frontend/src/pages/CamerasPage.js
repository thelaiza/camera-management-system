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
  const [editandoId, setEditandoId] = useState(null);
  const navigate = useNavigate();

  const buscarCameras = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/cameras/');
      setCameras(res.data);
    } catch (error) {
      console.error('Erro ao buscar câmeras:', error);
    }
  };

  useEffect(() => {
    buscarCameras();
  }, []);

  const abrirPopup = (camera = null) => {
    if (camera) {
      setEditandoId(camera.id);
      setNomeCamera(camera.nome);
      setLocalizacao(camera.localizacao);
      setStatus(camera.status || "pendente");
    } else {
      setEditandoId(null);
      setNomeCamera("");
      setLocalizacao("");
      setStatus("pendente");
    }
    setMostrarPopup(true);
  };

  const salvarCamera = async () => {
    const usuario_id = localStorage.getItem("usuario_id");

    try {
      if (editandoId) {
        await axios.put(`http://localhost:8000/api/cameras/${editandoId}/editar/`, {
          nome: nomeCamera,
          localizacao,
          status,
          usuario_id,
        });
      } else {
        await axios.post("http://localhost:8000/api/cameras/adicionar/", {
          nome: nomeCamera,
          localizacao,
          status,
          usuario_id,
        });
      }

      await buscarCameras();
      setMostrarPopup(false);
    } catch (error) {
      console.error("Erro ao salvar câmera:", error);
    }
  };

  const deletarCamera = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/cameras/excluir/${id}/`);
      buscarCameras();
    } catch (error) {
      console.error("Erro ao deletar câmera:", error);
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
          <div className="popup-content">
            <h3>{editandoId ? "Editar Câmera" : "Nova Câmera"}</h3>
            <input
              type="text"
              placeholder="Nome da câmera"
              value={nomeCamera}
              onChange={(e) => setNomeCamera(e.target.value)}
            />
            <input
              type="text"
              placeholder="Localização"
              value={localizacao}
              onChange={(e) => setLocalizacao(e.target.value)}
            />
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="instalada">🟢 Instalada</option>
              <option value="removida">🔴 Removida</option>
              <option value="pendente">🟡 Pendente</option>
            </select>
            <div className="popup-buttons">
              <button onClick={salvarCamera}>Salvar</button>
              <button onClick={() => setMostrarPopup(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}

      <div className="cameras-title-container">
        <h2 className="cameras-title">Câmeras</h2>
      </div>
      <div className="add-button-container">
        <button className="add-button" onClick={() => abrirPopup()}>Adicionar</button>
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
              <td>{camera.usuario_id || '-'}</td>
              <td className="actions">
                <span role="button" className="edit" onClick={() => abrirPopup(camera)}>✏️</span>
                <span role="button" className="delete" onClick={() => deletarCamera(camera.id)}>❌</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CamerasPage;
