import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/CamerasPage.css';
import { useNavigate } from "react-router-dom";

const CamerasPage = () => {
  const [cameras, setCameras] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost:8000/api/cameras/')
      .then(response => {
        setCameras(response.data);
      })
      .catch(error => {
        console.error('Erro ao buscar câmeras:', error);
      });
  }, []);

  return (
    <div className="cameras-container">
      <header className="cameras-header">
        <button className="back-button" onClick={() => navigate("/home")}>←</button>
        <img src="/logo.png" alt="Logo" className="logo" />
      </header>

      <div className="cameras-title-container">
        <h2 className="cameras-title">Câmeras</h2>
      </div>
      <div className="add-button-container">
  <button className="add-button">Adicionar</button>
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
