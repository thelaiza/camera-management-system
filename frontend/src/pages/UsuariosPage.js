import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/UsuariosPage.css';
import { useNavigate } from 'react-router-dom';

const UsuariosPage = () => {
  const [usuarios, setUsuarios] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost:8000/api/usuarios/')
      .then(response => {
        console.log("Dados recebidos do backend:", response.data);
        setUsuarios(response.data.usuarios);
          })
      .catch(error => {
        console.error('Erro ao buscar usuários:', error);
      });
  }, []);

  return (
    <div className="usuarios-container">
      <header className="usuarios-header">
        <button className="back-button" onClick={() => navigate('/home')}>←</button>
        <img src="/logo.png" alt="Logo" className="logo" />
      </header>

      <h2 className="usuarios-title">Usuários</h2>

      <div className="add-button-container">
        <button className="add-button">Adicionar</button>
      </div>

      <table className="usuarios-table">
  <thead>
    <tr>
      <th>ID</th>
      <th>Nome</th>
      <th>Email</th>
      <th>Nº de Câmeras</th>
      <th>Ações</th>
    </tr>
  </thead>
  <tbody>
    {Array.isArray(usuarios) && usuarios.map(usuario => (
      <tr key={usuario.id}>
        <td>{usuario.id}</td>
        <td>{usuario.nome}</td>
        <td>{usuario.email}</td>
        <td>{usuario.quantidade_cameras}</td> {/* ✅ Aqui estava o erro */}
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

export default UsuariosPage;
