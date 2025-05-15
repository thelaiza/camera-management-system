import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CamerasPage.css';
import { useNavigate } from 'react-router-dom';

const CamerasPage = () => {
  const [cameras, setCameras] = useState([]);
  const [mostrarPopup, setMostrarPopup] = useState(false);
  const [modoEdicao, setModoEdicao] = useState(false);
  const [cameraSelecionada, setCameraSelecionada] = useState(null);
  const [nome, setNome] = useState("");
  const [localizacao, setLocalizacao] = useState("");
  const [status, setStatus] = useState("pendente");
  const navigate = useNavigate();

  const carregarCameras = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/cameras/');
      setCameras(response.data);
    } catch (error) {
      console.error('Erro ao buscar câmeras:', error);
    }
  };

  useEffect(() => {
    carregarCameras();
  }, []);

  const abrirPopupAdicionar = () => {
    setModoEdicao(false);
    setNome("");
    setLocalizacao("");
    setStatus("pendente");
    setMostrarPopup(true);
  };

  const abrirPopupEditar = (camera) => {
    setModoEdicao(true);
    setCameraSelecionada(camera);
    setNome(camera.nome);
    setLocalizacao(camera.localizacao);
    setStatus(camera.status || "pendente");
    setMostrarPopup(true);
  };

  const handleSalvar = async () => {
  try {
    const usuario_id = localStorage.getItem("user_id");

    if (!usuario_id || usuario_id === "undefined") {
      alert("Usuário não autenticado. Faça login novamente.");
      navigate("/");
      return;
    }

    const payload = {
      nome,
      localizacao,
      status,
      usuario_id: Number(usuario_id)  
    };

    if (modoEdicao && cameraSelecionada) {
      await axios.put(
        `http://localhost:8000/api/cameras/${cameraSelecionada.id}/editar/`,
        payload
      );
    } else {
      await axios.post(
        "http://localhost:8000/api/cameras/adicionar/",
        payload
      );
    }

    setMostrarPopup(false);
    setNome("");
    setLocalizacao("");
    setStatus("pendente");
    setCameraSelecionada(null);
    carregarCameras();
  } catch (error) {
    console.error("Erro ao salvar câmera:", error);
  }
};


  const handleExcluir = async (id) => {
    if (window.confirm("Deseja realmente excluir esta câmera?")) {
      try {
        await axios.delete(`http://localhost:8000/api/cameras/excluir/${id}/`);
        carregarCameras();
      } catch (error) {
        console.error("Erro ao excluir câmera:", error);
      }
    }
  };

  return (
    <div className="cameras-container">
      <header className="cameras-header">
        <button className="back-button" onClick={() => navigate('/home')}>←</button>
        <img src="/logo.png" alt="Logo" className="logo" />
      </header>

      {mostrarPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <h3>{modoEdicao ? "Editar Câmera" : "Nova Câmera"}</h3>
            <input
              type="text"
              placeholder="Nome da câmera"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
            />
            <input
              type="text"
              placeholder="Localização"
              value={localizacao}
              onChange={(e) => setLocalizacao(e.target.value)}
            />
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="pendente">🟡 Pendente</option>
              <option value="instalada">🟢 Instalada</option>
              <option value="removida">🔴 Removida</option>
            </select>
            <div className="popup-buttons">
              <button onClick={handleSalvar}>Salvar</button>
              <button onClick={() => setMostrarPopup(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}

      <h2 className="cameras-title">Câmeras</h2>

      <div className="add-button-container">
        <button className="add-button" onClick={abrirPopupAdicionar}>Adicionar</button>
      </div>

      <table className="cameras-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Localização</th>
            <th>Status</th>
            <th>Usuário</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {cameras.map((camera) => (
            <tr key={camera.id}>
              <td>{camera.id}</td>
              <td>{camera.nome}</td>
              <td>{camera.localizacao}</td>
              <td>{camera.status}</td>
              <td>{camera.usuario_id || '-'}</td>
              <td className="actions">
                <span role="button" className="edit" onClick={() => abrirPopupEditar(camera)}>✏️</span>
                <span role="button" className="delete" onClick={() => handleExcluir(camera.id)}>❌</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CamerasPage;
