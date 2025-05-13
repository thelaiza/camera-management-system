import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CamerasPage.css';
import { useNavigate } from 'react-router-dom';

const CamerasPage = () => {
  const [cameras, setCameras] = useState([]);
  const [mostrarPopup, setMostrarPopup] = useState(false);
  const [nomeCamera, setNomeCamera] = useState("");
  const [localizacao, setLocalizacao] = useState("");
  const [status, setStatus] = useState("pendente");
  const navigate = useNavigate();

  useEffect(() => {
    buscarCameras();
  }, []);

  const buscarCameras = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/cameras/');
      setCameras(res.data);
    } catch (error) {
      console.error('Erro ao buscar câmeras:', error);
    }
  };

  const abrirPopup = (camera = null) => {
    if (camera) {
      setNomeCamera(camera.nome || "");
      setLocalizacao(camera.localizacao || "");
      setStatus(camera.status || "pendente");
    } else {
      setNomeCamera("");
      setLocalizacao("");
      setStatus("pendente");
    }
    setMostrarPopup(true);
  };

  const salvarCamera = async () => {
    const usuario_id = localStorage.getItem("usuario_id");
    if (!usuario_id) {
      alert("Usuário não autenticado. Faça login novamente.");
      navigate("/login");
      return;
    }

    try {
      await axios.post("http://localhost:8000/api/cameras/adicionar/", {
        nome: nomeCamera,
        localizacao,
        status,
        usuario_id
      });

      setNomeCamera("");
      setLocalizacao("");
      setStatus("pendente");
      setMostrarPopup(false);
      buscarCameras();
    } catch (error) {
      console.error("Erro ao salvar câmera:", error);
      alert("Erro ao salvar câmera. Verifique os dados e tente novamente.");
    }
  };

  const deletarCamera = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/cameras/excluir/${id}/`);
      buscarCameras();
    } catch (error) {
      console.error("Erro ao deletar câmera:", error);
      alert("Erro ao deletar câmera. Tente novamente.");
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
            <h3>Nova Câmera</h3>
            <input type="text" placeholder="Nome da câmera" value={nomeCamera} onChange={(e) => setNomeCamera(e.target.value)} />
            <input type="text" placeholder="Localização" value={localizacao} onChange={(e) => setLocalizacao(e.target.value)} />
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="pendente">🟡 Pendente</option>
              <option value="instalada">🟢 Instalada</option>
              <option value="removida">🔴 Removida</option>
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
        <button className="add-button" onClick={() => abrirPopup()}>Adicionar</button>
      </div>

      <table className="camera-table">
        <thead>
          <tr>
            <th>Status</th>
            <th>Nome</th>
            <th>Localização</th>
            <th>Usuário</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {cameras.map(camera => (
            <tr key={camera.id}>
              <td><span className={`dot ${camera.status}`}></span></td>
              <td>{camera.nome}</td>
              <td>{camera.localizacao}</td>
              <td>{camera.usuario_id || '-'}</td>
              <td className="actions">
                <button onClick={() => abrirPopup(camera)}>✏️</button>
                <button onClick={() => deletarCamera(camera.id)}>❌</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CamerasPage;
