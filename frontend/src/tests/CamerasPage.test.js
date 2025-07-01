import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import CamerasPage from '../pages/CamerasPage';

jest.mock('axios');

describe('CamerasPage Component', () => {
  test('renders cameras page title and add button', async () => {
    axios.get.mockResolvedValueOnce({ data: { cameras: [] } });
    render(
      <BrowserRouter>
        <CamerasPage />
      </BrowserRouter>
    );
    expect(await screen.findByText(/Câmeras/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Adicionar/i })).toBeInTheDocument();
  });

  test('displays cameras when API returns data', async () => {
    const mockCameras = {
        cameras: [
            { id: 1, nome: 'Camera Hall', localizacao: 'Entrada', status: 'ativa' },
            { id: 2, nome: 'Camera Garagem', localizacao: 'Subsolo', status: 'inativa' },
        ]
    };
    axios.get.mockResolvedValueOnce({ data: mockCameras });

    render(
      <BrowserRouter>
        <CamerasPage />
      </BrowserRouter>
    );
    expect(await screen.findByText('Camera Hall')).toBeInTheDocument();
    expect(await screen.findByText('Camera Garagem')).toBeInTheDocument();
  });
});