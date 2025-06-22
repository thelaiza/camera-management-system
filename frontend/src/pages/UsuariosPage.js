import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/UsuariosPage.css';
import { useNavigate } from 'react-router-dom';

const UsuariosPage = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [mostrarPopup, setMostrarPopup] = useState(false);
  const [modoEdicao, setModoEdicao] = useState(false);
  const [usuarioSelecionado, setUsuarioSelecionado] = useState(null);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const navigate = useNavigate();

  const carregarUsuarios = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/usuarios/');
      setUsuarios(response.data.usuarios);
    } catch (error) {
      console.error('Erro ao buscar usuários:', error);
    }
  };

  useEffect(() => {
    carregarUsuarios();
  }, []);

  const abrirPopupAdicionar = () => {
    setModoEdicao(false);
    setNome("");
    setEmail("");
    setSenha("");
    setMostrarPopup(true);
  };

  const abrirPopupEditar = (usuario) => {
    setModoEdicao(true);
    setUsuarioSelecionado(usuario);
    setNome(usuario.nome);
    setEmail(usuario.email);
    setSenha("");
    setMostrarPopup(true);
  };

  const handleSalvar = async () => {
    try {
      if (modoEdicao && usuarioSelecionado) {
        await axios.put(`http://localhost:8000/api/usuarios/editar/${usuarioSelecionado.id}/`, {
          nome,
          email,
          senha,
        });
      } else {
        const autor_id = localStorage.getItem("user_id");
        await axios.post("http://localhost:8000/api/usuarios/adicionar/", {
          nome,
          email,
          senha,
          autor_id: Number(autor_id)
        });
      }

      setMostrarPopup(false);
      setNome("");
      setEmail("");
      setSenha("");
      setUsuarioSelecionado(null);
      carregarUsuarios();
    } catch (error) {
      console.error("Erro ao salvar usuário:", error);
    }
  };

  const handleExcluir = async (id) => {
    const autor_id = localStorage.getItem("user_id");
    if (window.confirm("Deseja realmente excluir este usuário?")) {
      try {
        await axios.delete(`http://localhost:8000/api/usuarios/excluir/${id}/`, { 
            headers: { 'Content-Type': 'application/json' },
            data: { autor_id: Number(autor_id) } 
        });
        carregarUsuarios();
      } catch (error) {
        console.error("Erro ao excluir usuário:", error);
      }
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
            <h3>{modoEdicao ? "Editar Usuário" : "Novo Usuário"}</h3>
            <input
              type="text"
              placeholder="Nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
            />
            <input
              type="email"
              placeholder="E-mail"
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
              <button onClick={handleSalvar}>Salvar</button>
              <button onClick={() => setMostrarPopup(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}

      <h2 className="usuarios-title">Usuários</h2>

      <div className="add-button-container">
        <button className="add-button" onClick={abrirPopupAdicionar}>Adicionar</button>
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
          {usuarios.map((usuario) => (
            <tr key={usuario.id}>
              <td>{usuario.id}</td>
              <td>{usuario.nome}</td>
              <td>{usuario.email}</td>
              <td>{usuario.quantidade_cameras}</td>
              <td className="actions">
                <span role="button" className="edit" onClick={() => abrirPopupEditar(usuario)}>✏️</span>
                <span role="button" className="delete" onClick={() => handleExcluir(usuario.id)}>❌</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UsuariosPage;
