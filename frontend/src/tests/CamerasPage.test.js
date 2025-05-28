// frontend/src/tests/CamerasPage.test.js

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom'; // Se houver Links ou navegação
import CamerasPage from '../pages/CamerasPage'; // Ajuste o caminho
import axios from 'axios'; // Importe para mockar

// Mock para axios
jest.mock('axios');

// Mock para useNavigate, se CamerasPage ou seus modais usarem para navegação
const mockedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedNavigate,
}));


describe('CamerasPage Component', () => {
  beforeEach(() => {
    // Limpa mocks
    axios.get.mockClear();
    axios.post.mockClear();
    axios.put.mockClear();
    axios.delete.mockClear();
    mockedNavigate.mockClear();
  });

  test('renders cameras page title and add button', async () => {
    // Mock da resposta da API para a busca inicial de câmeras
    axios.get.mockResolvedValueOnce({ data: { cameras: [] } }); // Retorna uma lista vazia de câmeras

    render(
      <BrowserRouter>
        <CamerasPage />
      </BrowserRouter>
    );

    // Verifica o título da página
    expect(screen.getByText(/Câmeras/i)).toBeInTheDocument(); // O título "Câmeras" na sua página
    
    // Verifica o botão de adicionar
    expect(screen.getByRole('button', { name: /Adicionar/i })).toBeInTheDocument(); // Botão "Adicionar"

    // Espera que a chamada da API tenha sido feita
    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith('/api/cameras/'); // Endpoint de listagem de câmeras
    });
  });

  test('displays cameras when API returns data', async () => {
    const mockCameras = [
      { id: 1, nome: 'Camera Hall', localizacao: 'Entrada', status: 'ativa', usuario_responsavel: 'Laiza' },
      { id: 2, nome: 'Camera Garagem', localizacao: 'Subsolo', status: 'inativa', usuario_responsavel: 'Ana' },
    ];
    axios.get.mockResolvedValueOnce({ data: { cameras: mockCameras } });

    render(
      <BrowserRouter>
        <CamerasPage />
      </BrowserRouter>
    );

    // Espera que as câmeras sejam renderizadas na tela
    // Use waitFor para dar tempo para a chamada da API e a re-renderização
    expect(await screen.findByText('Camera Hall')).toBeInTheDocument();
    expect(await screen.findByText('Camera Garagem')).toBeInTheDocument();
    expect(screen.getByText('Entrada')).toBeInTheDocument();
    expect(screen.getByText('Subsolo')).toBeInTheDocument();
  });

  // Você adicionaria mais testes aqui, por exemplo:
  // - test('opens and closes add/edit modal')
  // - test('calls API to save a new camera')
  // - test('calls API to delete a camera')
});