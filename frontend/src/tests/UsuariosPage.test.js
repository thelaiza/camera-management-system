import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import UsuariosPage from '../pages/UsuariosPage';

jest.mock('axios');

describe('UsuariosPage Component', () => {
  beforeEach(() => {
    axios.get.mockClear();
  });

  test('renders usuarios page title and add button', async () => {
    axios.get.mockResolvedValueOnce({ data: { usuarios: [] } });
    render(
      <BrowserRouter>
        <UsuariosPage />
      </BrowserRouter>
    );

    expect(await screen.findByText(/Usuários/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Adicionar/i })).toBeInTheDocument();

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/usuarios/');
    });
  });

  test('displays usuarios when API returns data', async () => {
    const mockUsuarios = {
      usuarios: [
        { id: 1, nome: 'Laiza Silva', email: 'laiza@example.com', quantidade_cameras: 2 },
        { id: 2, nome: 'Ana Teste', email: 'ana@example.com', quantidade_cameras: 1 },
      ]
    };
    axios.get.mockResolvedValueOnce({ data: mockUsuarios });

    render(
      <BrowserRouter>
        <UsuariosPage />
      </BrowserRouter>
    );

    expect(await screen.findByText('Laiza Silva')).toBeInTheDocument();
    expect(await screen.findByText('ana@example.com')).toBeInTheDocument();
  });
});