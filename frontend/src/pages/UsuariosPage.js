import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/UsuariosPage.css';
import { useNavigate } from 'react-router-dom';

const UsuariosPage = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [mostrarPopup, setMostrarPopup] = useState(false);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const navigate = useNavigate();

  const buscarUsuarios = () => {
    axios.get('http://localhost:8000/api/usuarios/')
      .then(response => {
        setUsuarios(response.data.usuarios);
      })
      .catch(error => {
        console.error('Erro ao buscar usuários:', error);
      });
  };

  useEffect(() => {
    buscarUsuarios();
  }, []);

  const handleAdicionarUsuario = async () => {
    try {
      await axios.post("http://localhost:8000/api/usuarios/adicionar/", {
        nome,
        email,
        senha,
      });

      setNome("");
      setEmail("");
      setSenha("");
      setMostrarPopup(false);
      buscarUsuarios();
    } catch (error) {
      console.error("Erro ao adicionar usuário:", error);
    }
  };

  return (
    <div className="usuarios-container">
      <header className="usuarios-header">
        <button className="back-button" onClick={() => navigate('/home')}>←</button>
        <img src="/logo.png" alt="Logo" className="logo" />
      </header>

      {mostrarPopup && (
        <div className="popup-overlay">
          <div className="popup-content">
            <h3>Novo Usuário</h3>
            <input
              type="text"
              placeholder="Nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Senha"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
            />
            <div className="popup-buttons">
              <button onClick={handleAdicionarUsuario}>Salvar</button>
              <button onClick={() => setMostrarPopup(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}

      <h2 className="usuarios-title">Usuários</h2>

      <div className="add-button-container">
        <button className="add-button" onClick={() => setMostrarPopup(true)}>Adicionar</button>
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
              <td>{usuario.quantidade_cameras}</td>
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
