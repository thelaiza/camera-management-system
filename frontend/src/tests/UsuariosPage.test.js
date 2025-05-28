// frontend/src/tests/UsuariosPage.test.js

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom'; // Se houver Links ou navegação
import UsuariosPage from '../pages/UsuariosPage'; // Ajuste o caminho
import axios from 'axios'; // Importe para mockar

// Mock para axios
jest.mock('axios');

// Mock para useNavigate, se UsuariosPage ou seus modais usarem para navegação
const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedNavigate,
}));

describe('UsuariosPage Component', () => {
  beforeEach(() => {
    // Limpa mocks
    axios.get.mockClear();
    axios.post.mockClear();
    axios.put.mockClear();
    axios.delete.mockClear();
    mockedNavigate.mockClear();
  });

  test('renders usuarios page title and add button', async () => {
    // Mock da resposta da API para a busca inicial de usuários
    axios.get.mockResolvedValueOnce({ data: { usuarios: [] } }); // Retorna uma lista vazia de usuários

    render(
      <BrowserRouter>
        <UsuariosPage />
      </BrowserRouter>
    );

    // Verifica o título da página
    expect(screen.getByText(/Usuários/i)).toBeInTheDocument(); // O título "Usuários" na sua página
    
    // Verifica o botão de adicionar
    expect(screen.getByRole('button', { name: /Adicionar/i })).toBeInTheDocument(); // Botão "Adicionar"

    // Espera que a chamada da API tenha sido feita
    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith('/api/usuarios/'); // Endpoint de listagem de usuários
    });
  });

  test('displays usuarios when API returns data', async () => {
    const mockUsuarios = [
      { id: 1, nome: 'Laiza Silva', email: 'laiza@example.com', qtd_cameras: 3 },
      { id: 2, nome: 'Ana Teste', email: 'ana@example.com', qtd_cameras: 1 },
    ];
    // Sua API para usuários retorna uma lista diretamente, não um objeto com a chave 'usuarios'
    // como em CamerasPage. Ajuste o mock e a forma como o componente consome os dados se necessário.
    // No seu UsuariosPage.js, você faz: setUsuarios(response.data.usuarios || []);
    // Então o mock deve ser { data: { usuarios: mockUsuarios } }
    axios.get.mockResolvedValueOnce({ data: { usuarios: mockUsuarios } });


    render(
      <BrowserRouter>
        <UsuariosPage />
      </BrowserRouter>
    );

    expect(await screen.findByText('Laiza Silva')).toBeInTheDocument();
    expect(await screen.findByText('ana@example.com')).toBeInTheDocument(); // Email do segundo usuário
  });

  // Você adicionaria mais testes aqui, por exemplo:
  // - test('opens and closes add/edit modal for usuarios')
  // - test('calls API to save a new usuario')
  // - test('calls API to delete a usuario')
});